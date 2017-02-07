# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    请使用命令: python JDiOSExcelFromDir.py <iPad/iPhone> <fileDirs,....>
    对指定文件夹下的所有json文件进行递归查找并且添加到相应的list中,最后归类到相应的表格中
    文件输出名字:dirName.xlsx
"""

import json
import os
import sys
import xlsxwriter

import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False

global_iPad_name = "Jdipad"
global_iPone_name = "JD4iPhone"

# 设备输出表列表字段索引
crashThreadIndexIndex = 0           # 崩溃线程索引
iosVersionIndex = 1                 # 系统版本
archIndex = 2                       # 设备架构
diagnosisIndex = 3                  # 诊断信息
applicationInForegroundIndex = 4    # 前台状态
applicationActiveIndex = 5          # 活跃状态

processIndex = 6                    # process信息
crashThreadSymbolListIndex = 7      # 崩溃调用栈信息
mainThreadSymbolListIndex = 8       # 崩溃调用栈信息

notableAddressIndex = 9             # 崩溃地址信息

event_historyIndex = 10             # 事件发生记录
nav_historyIndex = 11               # 页面访问记录
url_historyIndex = 12               # 网页访问记录
crashFileNameIndex = 13             # 源文件名称


# ----------------------------------  函数定义区 --------------------------------------- #

def needExcelDir(input_filedir_list):
    # 文件归类完成后,再使用excel整理
    # 创建相关的 excel 文件
    # 生成需要解析为excel的文件夹,带上路径名

    if not CJFKit.validateList(input_filedir_list):
        return

    # 此处表示多文件夹输入
    for excelElementDirName in input_filedir_list:

        # 此处表示获取该文件夹下所有的.json文件
        needExcelFileList = CJFKit.recursionGetSpecialFilesInSpecialDir(excelElementDirName, "*.json", True, True)
        if not CJFKit.validateList(needExcelFileList):
            continue

        outFilePath = excelElementDirName + ".xlsx"
        outFile = xlsxwriter.Workbook(outFilePath)
        outTable = outFile.add_worksheet('Crash')

        # 输出格式创建,目前专注于使用xlsx
        titleStyle1 = outFile.add_format(
                {'border':1, 'align':'center', 'bg_color':'green', 'font_size':13, 'bold':True})
        titleStyle2 = outFile.add_format({'border':1, 'align':'center', 'bg_color':'blue', 'font_size':13, 'bold':True})
        contentCenterStyle = outFile.add_format({'align':'center', 'font_size':12})
        contentLeftStyle = outFile.add_format({'font_size':12})
        # contentLightStyle = outFile.add_format({'align':'center', 'bg_color':'yellow', 'font_size':12})

        # 设置列宽
        outTable.set_column(crashThreadIndexIndex, crashThreadIndexIndex, 10)
        outTable.set_column(iosVersionIndex, iosVersionIndex, 15)
        outTable.set_column(archIndex, archIndex, 10)
        outTable.set_column(diagnosisIndex, diagnosisIndex, 50)
        outTable.set_column(applicationInForegroundIndex, applicationActiveIndex, 10)
        outTable.set_column(processIndex, processIndex, 20)
        outTable.set_column(crashThreadSymbolListIndex, mainThreadSymbolListIndex, 50)
        outTable.set_column(notableAddressIndex, notableAddressIndex, 20)
        outTable.set_column(event_historyIndex, url_historyIndex, 50)
        outTable.set_column(crashFileNameIndex, crashFileNameIndex, 40)

        # 设置输出表 CrashLog 列表字段title
        outTable.write_string(0, crashThreadIndexIndex, "thread", titleStyle1)
        outTable.write_string(0, iosVersionIndex, "iosVersion", titleStyle2)
        outTable.write_string(0, archIndex, "arch", titleStyle1)
        outTable.write_string(0, diagnosisIndex, "diagnosis", titleStyle2)
        outTable.write_string(0, applicationInForegroundIndex, "appFG", titleStyle1)
        outTable.write_string(0, applicationActiveIndex, "appAT", titleStyle2)
        outTable.write_string(0, processIndex, "process", titleStyle1)
        outTable.write_string(0, crashThreadSymbolListIndex, "crashThreadSymbolList", titleStyle2)
        outTable.write_string(0, mainThreadSymbolListIndex, "mainThreadSymbolList", titleStyle1)
        outTable.write_string(0, notableAddressIndex, "notableAddress", titleStyle2)
        outTable.write_string(0, event_historyIndex, "last_event_history", titleStyle1)
        outTable.write_string(0, nav_historyIndex, "last_nav_history", titleStyle2)
        outTable.write_string(0, url_historyIndex, "last_url_history", titleStyle1)
        outTable.write_string(0, crashFileNameIndex, "crashFileName", titleStyle2)

        needExcelFileIndex = 1
        for needExcelFileName in needExcelFileList:

            needExcelFileStr = CJFKit.safeGetFileContentStr(needExcelFileName, True)
            if not CJFKit.validateString(needExcelFileStr):
                print "Error: file %s content is empty." % needExcelFileName
                continue

            try:
                needClassifyFileJson = json.loads(needExcelFileStr)
            except:
                print "Error: file %s json decode is error." % needExcelFileName
                continue

            crashThreadIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [0, "crashThreadIndex"])
            if CJFKit.validateNumber(crashThreadIndexContent):
                crashThreadIndexContent = "%d" % crashThreadIndexContent
            else:
                crashThreadIndexContent = "unknow"
            outTable.write_string(needExcelFileIndex, crashThreadIndexIndex, crashThreadIndexContent,
                                  contentCenterStyle)

            iosVersionIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "system_version"])
            if not CJFKit.validateString(iosVersionIndexContent):
                iosVersionIndexContent = "unknow"
            outTable.write_string(needExcelFileIndex, iosVersionIndex, iosVersionIndexContent, contentCenterStyle)

            archIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "cpu_arch"])
            if not CJFKit.validateString(archIndexContent):
                archIndexContent = "unknow"
            outTable.write_string(needExcelFileIndex, archIndex, archIndexContent, contentCenterStyle)

            diagnosisIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [0, "diagnosis"])
            if not CJFKit.validateString(diagnosisIndexContent):
                diagnosisIndexContent = ""
            outTable.write_string(needExcelFileIndex, diagnosisIndex, diagnosisIndexContent, contentLeftStyle)

            applicationInForegroundIndexContent = CJFKit.safeGetElement(needClassifyFileJson,
                                                                        [0, "system", "application_stats",
                                                                         "application_in_foreground"])
            if isinstance(applicationInForegroundIndexContent, bool) and applicationInForegroundIndexContent:
                applicationInForegroundIndexContent = "true"
            else:
                applicationInForegroundIndexContent = ""
            outTable.write_string(needExcelFileIndex, applicationInForegroundIndex, applicationInForegroundIndexContent,
                                  contentCenterStyle)

            applicationActiveIndexContent = CJFKit.safeGetElement(needClassifyFileJson,
                                                                  [0, "system", "application_stats",
                                                                   "application_active"])
            if isinstance(applicationActiveIndexContent, bool) and applicationActiveIndexContent:
                applicationActiveIndexContent = "true"
            else:
                applicationActiveIndexContent = ""
            outTable.write_string(needExcelFileIndex, applicationActiveIndex, applicationActiveIndexContent,
                                  contentCenterStyle)

            processIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [1, "process"])
            if not CJFKit.validateList(processIndexContent):
                processIndexContent = "none"
            else:
                processIndexContent = json.dumps(processIndexContent, indent = 4)
            outTable.write_string(needExcelFileIndex, processIndex, processIndexContent, contentCenterStyle)

            crashThreadSymbolListIndexContent = CJFKit.safeGetElement(needClassifyFileJson,
                                                                      [1, "crashThreadSymbolList"])
            if not CJFKit.validateList(crashThreadSymbolListIndexContent):
                crashThreadSymbolListIndexContent = ""
            else:
                crashThreadSymbolListIndexContent = json.dumps(crashThreadSymbolListIndexContent, indent = 4)
            outTable.write_string(needExcelFileIndex, crashThreadSymbolListIndex, crashThreadSymbolListIndexContent,
                                  contentLeftStyle)

            mainThreadSymbolListIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [1, "mainThreadSymbolList"])
            if not CJFKit.validateList(mainThreadSymbolListIndexContent):
                mainThreadSymbolListIndexContent = ""
            else:
                mainThreadSymbolListIndexContent = json.dumps(mainThreadSymbolListIndexContent, indent = 4)
            outTable.write_string(needExcelFileIndex, mainThreadSymbolListIndex, mainThreadSymbolListIndexContent,
                                  contentLeftStyle)

            notableAddressIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [2, "notableAddress"])
            if not CJFKit.validateDictionary(notableAddressIndexContent):
                notableAddressIndexContent = ""
            else:
                # 精简excel输出
                # notableAddressIndexContent = json.dumps(notableAddressIndexContent, indent = 4)
                notableAddressIndexContent = "have"
            outTable.write_string(needExcelFileIndex, notableAddressIndex, notableAddressIndexContent,
                                  contentCenterStyle)

            event_historyIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [3, "user", "event_history"])
            if not CJFKit.validateList(event_historyIndexContent):
                event_historyIndexContent = ""
            else:
                event_historyIndexContent = event_historyIndexContent[-1]
                event_historyIndexContent = json.dumps(event_historyIndexContent, indent = 4)
            outTable.write_string(needExcelFileIndex, event_historyIndex, event_historyIndexContent, contentLeftStyle)

            nav_historyIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [3, "user", "nav_history"])
            if not CJFKit.validateList(nav_historyIndexContent):
                nav_historyIndexContent = ""
            else:
                nav_historyIndexContent = nav_historyIndexContent[-1]
                nav_historyIndexContent = json.dumps(nav_historyIndexContent, indent = 4)
            outTable.write_string(needExcelFileIndex, nav_historyIndex, nav_historyIndexContent, contentLeftStyle)

            url_historyIndexContent = CJFKit.safeGetElement(needClassifyFileJson, [3, "user", "url_history"])
            if not CJFKit.validateList(url_historyIndexContent):
                url_historyIndexContent = ""
            else:
                url_historyIndexContent = url_historyIndexContent[-1]
                url_historyIndexContent = json.dumps(url_historyIndexContent, indent = 4)
            outTable.write_string(needExcelFileIndex, url_historyIndex, url_historyIndexContent, contentLeftStyle)

            needExcelFileName = os.path.basename(needExcelFileName)
            needExcelFileName = CJFKit.toValidateString(needExcelFileName)
            outTable.write_string(needExcelFileIndex, crashFileNameIndex, needExcelFileName, contentCenterStyle)

            # 写入行号递增
            needExcelFileIndex += 1

        # 单个文件夹写入结束保存excel
        outFile.close()
    return


# ----------------------------------  正式代码区域 -------------------------------------- #

if __name__ == "__main__":
    target_name = ""
    target_input_filedir_list = []

    if not target_debug_flag:
        if len(sys.argv) >= 3:
            appName = sys.argv[1]
            if appName == "iPhone":
                target_name = global_iPone_name
            else:
                target_name = global_iPad_name
            for index in range(2, len(sys.argv)):
                target_input_filedir_list.append(sys.argv[index])
        else:
            print "Error: need origin fileDir Param. Please use : python JDiPadCrashParser.py <fileDir,...>"
            sys.exit(-1)
    else:
        target_name = global_iPad_name
        target_input_filedir_list.append("../iPad_380_1002/sortOut/crash_symbol")
        target_input_filedir_list.append("../iPad_380_1002/sortOut/crash_system")
    needExcelDir(target_input_filedir_list)
