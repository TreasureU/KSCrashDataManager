# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    请使用命令: python JDiOSCrashSortOutRecursion.py <iPad/iPhone> <fileDir>
    脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.
    脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
    如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import glob
import json
import os
import sys

import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False

# 关键字映射文件
global_crash_keyword_mapping_iPadfileName = "./setting/systemKeyWordMappingiPad.json"
global_crash_keyword_mapping_iPhonefileName = "./setting/systemKeyWordMappingiPhone.json"
target_crash_keyword_mapping_fileName = None

global_crash_keyword_mapping = None

# 关键功能参数表
# 子文件夹按照controller排列,并输出单独的报告
classifyByController = "classifyByController"


# ----------------------------------   类定义区  --------------------------------------- #


# ----------------------------------  函数定义区 --------------------------------------- #

def safeSymbolLinkCrashFile(fileName, dstName, dirName = "../../.."):
    # global target_input_filedir
    fileName = dirName + "/parser/" + fileName
    CJFKit.safeSymbolLink(fileName, dstName)


def classifyByControllerMethod(compareModel, fileName, fileJson):
    global target_input_filedir
    global classifyByController
    last_nav_history = CJFKit.safeGetElement(fileJson, [-1, "user", "nav_history", -1, "c"])
    if not CJFKit.validateString(last_nav_history):
        last_nav_history = "None"
    CJFKit.safeCreateDir(
            target_input_filedir + "/sortOut/crash_system/" + compareModel.fileDirName + "/" + last_nav_history)
    compareModel.addController(last_nav_history)
    myoutputFileName = target_input_filedir + "/sortOut/crash_system/" + compareModel.fileDirName + "/" + last_nav_history + "/" + os.path.basename(
            fileName)
    safeSymbolLinkCrashFile(os.path.basename(fileName), myoutputFileName, "../../../..")


# ----------------------------------  正式代码区域 -------------------------------------- #

if not target_debug_flag:
    if len(sys.argv) >= 3:
        appName = sys.argv[1]
        if appName == "iPhone":
            target_crash_keyword_mapping_fileName = global_crash_keyword_mapping_iPhonefileName
        else:
            target_crash_keyword_mapping_fileName = global_crash_keyword_mapping_iPadfileName
        target_input_filedir = sys.argv[2]
    else:
        print "Error: need origin fileDir Param. Please use : python xxipadCrashParser.py <fileDir>"
        sys.exit(-1)
else:
    target_crash_keyword_mapping_fileName = global_crash_keyword_mapping_iPadfileName
    target_input_filedir = "../ap_mon"

if os.path.isfile(target_crash_keyword_mapping_fileName):
    global_crash_keyword_mapping = CJFKit.safeGetFileContentJSON(target_crash_keyword_mapping_fileName, True)

if not CJFKit.validateList(global_crash_keyword_mapping):
    print "Error: global_crash_keyword_mapping build error."
    sys.exit(-1)

# 新建分类文件夹
CJFKit.safeClearDir(target_input_filedir + "/sortOut/" + "crash_system")

singleParamReportDic = {}

global_crash_Mapping_list = []

# 初始化分类文件夹
for searchPair in global_crash_keyword_mapping:
    tmpModel = CJFKit.systemCrashModel.dictToSystemCrashModel(searchPair)
    if tmpModel:
        global_crash_Mapping_list.append(tmpModel)

not_match_model = CJFKit.systemCrashModel("", "not_matched")
not_match_model.description = "can matched crash"
not_match_model.param = {classifyByController:True}
not_match_model.controllers = {}
CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_system/" + not_match_model.fileDirName)

file_error_count = 0
file_error_list = []

needClassifyFileList = glob.glob(target_input_filedir + "/sortOut/not_sortOut/*.json")
allFileCount = len(needClassifyFileList)
if allFileCount <= 0:
    print "Warning: %s/sortOut/not_sortOut is no *.json file" % target_input_filedir
    sys.exit(-1)

for needClassifyFileName in needClassifyFileList:
    needClassifyFileStr = CJFKit.safeGetFileContentStr(needClassifyFileName, True)
    if not CJFKit.validateString(needClassifyFileStr):
        print "Error: file %s content is empty." % needClassifyFileName
        file_error_count += 1
        file_error_list.append(needClassifyFileName)
        continue

    try:
        needClassifyFileJson = json.loads(needClassifyFileStr)
    except:
        print "Error: file %s json decode is error." % needClassifyFileName
        file_error_count += 1
        file_error_list.append(needClassifyFileName)
        continue

    activeTimeSinceLaunch = CJFKit.safeGetElement(needClassifyFileJson,
                                                  [0, "system", "application_stats", "active_time_since_launch"])
    if not CJFKit.validateNumber(activeTimeSinceLaunch):
        activeTimeSinceLaunch = 0.0
    elif activeTimeSinceLaunch < 0:
        activeTimeSinceLaunch = 0.0

    bgTimeSinceLaunch = CJFKit.safeGetElement(needClassifyFileJson,
                                              [0, "system", "application_stats", "background_time_since_launch"])
    if not CJFKit.validateNumber(bgTimeSinceLaunch):
        bgTimeSinceLaunch = 0.0
    elif bgTimeSinceLaunch < 0.0:
        bgTimeSinceLaunch = 0.0

    for systemCompareModel in global_crash_Mapping_list:

        # 匹配多个关键字的情况
        if CJFKit.validateString(systemCompareModel.fileDirName) and CJFKit.validateList(systemCompareModel.keyWords):
            # 校验是否符合情况
            findCount = 0
            for needFindKey in systemCompareModel.keyWords:
                if needFindKey in needClassifyFileStr:
                    findCount += 1
            if findCount == len(systemCompareModel.keyWords):
                systemCompareModel.count += 1
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_system/" + systemCompareModel.fileDirName)
                # 附加参数处理区
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_system/" + systemCompareModel.fileDirName + "/" + os.path.basename(
                            needClassifyFileName)
                    safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName, "../../..")
                osVersion = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "system_version"])
                if not osVersion:
                    osVersion = "None"
                systemCompareModel.addOSversion(osVersion)

                deviceType = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "machine"])
                if not deviceType:
                    deviceType = "None"
                systemCompareModel.addDeviceType(deviceType)

                mwTimeInterval = CJFKit.safeGetElement(needClassifyFileJson, [0, "mwTimeInterval"])
                systemCompareModel.addMWTimerInterval(mwTimeInterval)
                systemCompareModel.addATTimerInterval(activeTimeSinceLaunch)
                systemCompareModel.addBGTimerInterval(bgTimeSinceLaunch)
                break

        # 匹配到使用单一关键字的情况
        elif CJFKit.validateString(systemCompareModel.fileDirName) and CJFKit.validateString(
                systemCompareModel.keyWord):
            # 校验是否符合情况
            if systemCompareModel.keyWord in needClassifyFileStr:
                systemCompareModel.count += 1
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_system/" + systemCompareModel.fileDirName)
                # 附加参数处理区
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_system/" + systemCompareModel.fileDirName + "/" + os.path.basename(
                            needClassifyFileName)
                    safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName, "../../..")
                osVersion = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "system_version"])
                if not osVersion:
                    osVersion = "None"
                systemCompareModel.addOSversion(osVersion)

                deviceType = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "machine"])
                if not deviceType:
                    deviceType = "None"
                systemCompareModel.addDeviceType(deviceType)

                mwTimeInterval = CJFKit.safeGetElement(needClassifyFileJson, [0, "mwTimeInterval"])
                systemCompareModel.addMWTimerInterval(mwTimeInterval)
                systemCompareModel.addATTimerInterval(activeTimeSinceLaunch)
                systemCompareModel.addBGTimerInterval(bgTimeSinceLaunch)
                break

        elif CJFKit.validateString(systemCompareModel.fileDirName) and CJFKit.validateList(
                systemCompareModel.keyWordList):
            foundFlag = False
            for needFindKey in systemCompareModel.keyWordList:
                if needFindKey in needClassifyFileStr:
                    foundFlag = True
                    break
            if foundFlag:
                systemCompareModel.count += 1
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_system/" + systemCompareModel.fileDirName)
                # 附加参数处理区
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_system/" + systemCompareModel.fileDirName + "/" + os.path.basename(
                            needClassifyFileName)
                    safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName, "../../..")
                osVersion = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "system_version"])
                if not osVersion:
                    osVersion = "None"
                systemCompareModel.addOSversion(osVersion)

                deviceType = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "machine"])
                if not deviceType:
                    deviceType = "None"
                systemCompareModel.addDeviceType(deviceType)

                mwTimeInterval = CJFKit.safeGetElement(needClassifyFileJson, [0, "mwTimeInterval"])
                systemCompareModel.addMWTimerInterval(mwTimeInterval)
                systemCompareModel.addATTimerInterval(activeTimeSinceLaunch)
                systemCompareModel.addBGTimerInterval(bgTimeSinceLaunch)
                break
    else:
        # 直接写入未匹配文件夹
        not_match_model.count += 1
        classifyByControllerMethod(not_match_model, needClassifyFileName, needClassifyFileJson)

global_crash_Mapping_result_list = []
for tmpModel in global_crash_Mapping_list:
    # 输出全部报告的地方
    tmpModel.percentage = tmpModel.count * 100.0 / allFileCount
    CJFKit.safeWriteFileContentJSON(
            target_input_filedir + "/sortOut/crash_system/" + tmpModel.fileDirName + "/assitInfo",
            tmpModel.getCrashAssitInfo())
    global_crash_Mapping_result_list.append(tmpModel.convertToDict())

result_glance_list = []
noMatchDic = {
    "fileDirName":"not_matched",
    "keyWord":None,
    "count":not_match_model.count,
    "perCentage":(not_match_model.count * 100.0 / allFileCount)}
allFileDic = {"fileDirName":"all_file",
              "keyWord":None,
              "count":allFileCount,
              "perCentage":100.0}
errorFileDic = {"fileDirName":"error_file",
                "keyWord":None,
                "count":file_error_count,
                "perCentage":(file_error_count * 100.0 / allFileCount)}
result_glance_list.append(allFileDic)
result_glance_list.append(noMatchDic)
result_glance_list.append(errorFileDic)

# 统一数据排序
global_crash_Mapping_result_list.sort(key = lambda x:x["percentage"], reverse = True)
result_glance_list.append({"crash sort":global_crash_Mapping_result_list})

sub_crash_sort_list = []
for tmpModel in global_crash_Mapping_list:
    if CJFKit.validateDictionary(tmpModel.controllers):
        sub_crash_sort_list.append({"name":tmpModel.description, "result":tmpModel.controllers})

sub_crash_sort_list.append({"name":"not_matched", "result":not_match_model.controllers})
result_glance_list.append({"sub crash sort by controller":sub_crash_sort_list})

result_glance_list.append({"error_file_list":file_error_list})
CJFKit.safeWriteFileContentJSON(target_input_filedir + "/sortOut/SortOutRecursionResult", result_glance_list, True,
                                True)

print "Recursion sortOut is done"
print "Result report is output in SortOutRecursionResult"
