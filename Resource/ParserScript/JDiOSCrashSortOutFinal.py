# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    请使用命令: python JDiOSCrashSortOutFinal.py <iPad/iPhone> <fileDir>
    脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.
    脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
    如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
    归类依据:
        1.先判断 crashThread 中有无归属于 xxipad 的类信息,有的话,那么就按照这个输出分配。
        2.再判断 userInfo 中的最后一个页面归属于何方
        3.输出整体报表.
    注意:在 not_sort 中也会包含 crash_controller 的信息,但不参与计数工作
"""

import os
import sys
import time

import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False

target_use_old_mainVC_filter = True

# old
target_mainVC_min_limit = 10
target_mainVC_per = 0.6

# new
target_mainVC_needCount = 3

# 数据对比
target_compare_dirName = None
target_compare_Json = None

global_iPad_name = "xxipad"
global_iPhone_name = "xxxiPhone"


# ----------------------------------  函数定义区 --------------------------------------- #

def safeSymbolLinkCrashFile(fileName, dstName, dirName):
    # global target_input_filedir
    fileName = dirName + "/parser/" + fileName
    CJFKit.safeSymbolLink(fileName, dstName)


# ----------------------------------  类定义区域 -------------------------------------- #


# ----------------------------------  正式代码区域 -------------------------------------- #

timeStart = time.time()

target_name = ""
target_input_filedir = ""

if not target_debug_flag:
    if len(sys.argv) >= 3:
        appName = sys.argv[1]
        if appName == "iPhone":
            target_name = global_iPhone_name
        else:
            target_name = global_iPad_name
        target_input_filedir = sys.argv[2]

        if len(sys.argv) >= 4:
            target_compare_dirName = sys.argv[3]

    else:
        print "Error: need origin fileDir Param. Please use : python xxipadCrashParser.py <fileDir>"
        sys.exit(-1)
else:
    target_name = global_iPhone_name
    target_input_filedir = "../iPhone_21"
    target_compare_dirName = "../iPhone_20"

need_remove_crash_fileList = []
need_check_crash_fileList = []

# 此时这里的文件一般可以认为是无效的,当然,如果没人愿意去做递归,那么就不会走到这一步
CJFKit.safeRemovePath(target_input_filedir + "/sortOut/crash_controller")
CJFKit.safeRemovePath(target_input_filedir + "/sortOut/not_sortOut")

# 所有解析出来的数据排序
sort_out_init_list = CJFKit.safeGetFileContentJSON(target_input_filedir + "/sortOut/SortOutInitResult")

sort_out_recursion_exist = True
sort_out_recursion_list = CJFKit.safeGetFileContentJSON(target_input_filedir + "/sortOut/SortOutRecursionResult")

if not CJFKit.validateList(sort_out_init_list):
    print "Error: decode SortOutInitResult error,please check these"
    sys.exit(-1)

if not CJFKit.validateList(sort_out_recursion_list):
    print "Warnning: decode SortOutRecursionResult error,please check these"
    sort_out_recursion_exist = False

self_init_list = sort_out_init_list[0]["result glance"]
if sort_out_recursion_exist:
    system_allfile_list = sort_out_recursion_list[0]
    not_matched_count_dic = sort_out_recursion_list[1]
    error_file_count_dic = sort_out_recursion_list[2]
else:
    system_allfile_list = {
        "count":0,
        "fileDirName":"all_file",
        "perCentage":0.0,
        "keyWord":None
    }
    not_matched_count_dic = {
        "count":0,
        "fileDirName":"not_matched",
        "perCentage":0.0,
        "keyWord":None
    }
    error_file_count_dic = {
        "count":0,
        "fileDirName":"error_file",
        "perCentage":0.0,
        "keyWord":None
    }

all_file_count = self_init_list[0]["count"]

system_crash_count_dic = {
    "count":system_allfile_list["count"] - not_matched_count_dic["count"],
    "name":"paired system crash result",
    "percentage":(system_allfile_list["count"] - not_matched_count_dic["count"]) * 100.0 / all_file_count
}
not_matched_count_dic = {
    "count":not_matched_count_dic["count"],
    "name":"no match crash result",
    "percentage":not_matched_count_dic["count"] * 100.0 / all_file_count,
    "fileDirName":"sortOut/crash_system/not_matched"
}
error_file_count_dic = {
    "count":error_file_count_dic["count"] + self_init_list[4]["count"],
    "name":"file error result",
    "percentage":(error_file_count_dic["count"] + self_init_list[4]["count"]) * 100.0 / all_file_count
}

if sort_out_recursion_exist:
    system_crash_list = sort_out_recursion_list[3]["crash sort"]
else:
    system_crash_list = []

canfix_system_crash_count = 0
for system_crash_model in system_crash_list:
    if system_crash_model["canFix"]:
        canfix_system_crash_count += system_crash_model["count"]
canfix_system_crash_count += self_init_list[1]["count"]
canfix_percentage_dic = {
    "name":"can fix",
    "count":canfix_system_crash_count,
    "percentage":canfix_system_crash_count * 100.0 / all_file_count
}

# 新建结果列表输出格式
all_sort_result_reports = []
for symbolDic in sort_out_init_list[1]["symbol crash sort result"]:
    tmpDic = {"name":symbolDic["description"],
              "count":symbolDic["count"],
              "canFix":symbolDic["canFix"],
              "fileDirName":"sortOut/crash_symbol/" + symbolDic["fileDirName"],
              "percentage":symbolDic["count"] * 100.0 / all_file_count}
    all_sort_result_reports.append(tmpDic)

for systemDic in system_crash_list:
    tmpDic = {"name":systemDic["description"],
              "count":systemDic["count"],
              "canFix":systemDic["canFix"],
              "fileDirName":"sortOut/crash_system/" + systemDic["fileDirName"],
              "percentage":systemDic["count"] * 100.0 / all_file_count}
    all_sort_result_reports.append(tmpDic)

all_sort_result_reports.append(not_matched_count_dic)
all_sort_result_reports.append(error_file_count_dic)

all_sort_result_reports.sort(key = lambda x:x["count"], reverse = True)

result_list = [self_init_list[0], self_init_list[1]]

if len(self_init_list) == 6:
    result_list.append(self_init_list[5])   # BG crash file

result_list.append(system_crash_count_dic)  # system crash file
result_list.append(not_matched_count_dic)   # not matched crash file
result_list.append(error_file_count_dic)    # error file
result_list.append(canfix_percentage_dic)   # can fix percentage

# 最终输出拼接
out_put_result_list = [
    {
        "result glance":result_list
    },
    {
        "all result report":all_sort_result_reports
    }
]

out_file_name = target_input_filedir + "/sortOut/SortOutFinalResult"
CJFKit.safeWriteFileContentJSON(out_file_name, out_put_result_list)

if len(self_init_list) == 6:
    all_sort_result_reports_str = "*" + "\t" + "BG" + "\t" + (
        "%.2f" % self_init_list[5]["percentage"]) + "\t" + "sortOut/BG\n"
else:
    all_sort_result_reports_str = ""

final_controller_dic = {}
tmpDic = sort_out_init_list[2]["symbol crash controller sort result"]
final_controller_dic.update(tmpDic)
if sort_out_recursion_exist:
    tmpList = sort_out_recursion_list[4]["sub crash sort by controller"]
    if CJFKit.validateList(tmpList):
        for tmpDic in tmpList:
            final_controller_dic[tmpDic["name"]] = tmpDic["result"]

if CJFKit.validateString(target_compare_dirName):
    if os.path.isfile(target_compare_dirName + "/sortOut/SortOutFinalResult"):
        target_compare_Json = CJFKit.safeGetFileContentJSON(target_compare_dirName + "/sortOut/SortOutFinalResult")
        if CJFKit.validateList(target_compare_Json):
            target_compare_Json = CJFKit.safeGetElement(target_compare_Json, [1, "all result report"])
        if not CJFKit.validateList(target_compare_Json):
            target_compare_Json = None

i = 1
for report_dic in all_sort_result_reports:
    name = report_dic["name"]
    if name[-1] == "\n":
        name = name[:-1]
    fileDirName = CJFKit.safeGetDicElement(report_dic, "fileDirName")
    if not CJFKit.validateString(fileDirName):
        fileDirName = "None"

    controllers_dic = CJFKit.safeGetDicElement(final_controller_dic, name)
    max_controller_name = ""
    if CJFKit.validateDictionary(controllers_dic):
        single_count = 0
        for keyName in controllers_dic.keys():
            single_count += controllers_dic[keyName]
        if target_use_old_mainVC_filter and single_count >= target_mainVC_min_limit:
            for keyName in controllers_dic.keys():
                if controllers_dic[keyName] >= (single_count * target_mainVC_per):
                    max_controller_name += ("(%s_%.2f)" % (keyName, controllers_dic[keyName] * 1.0 / single_count))
        elif not target_use_old_mainVC_filter:
            single_controllers_sort_list = CJFKit.systemCrashModel.getSortListFormDict(controllers_dic)
            if CJFKit.validateList(single_controllers_sort_list):
                min_list_value = min(target_mainVC_needCount, len(single_controllers_sort_list))
            for index in range(0, min_list_value):
                max_controller_name += ("(%s_%.2f)" % (
                single_controllers_sort_list[index]["name"], single_controllers_sort_list[index]["percentage"]))
        else:
            pass

    # 默认变化值为本次崩溃率占比
    perChangeStr = "%.2f" % (report_dic["percentage"])
    if target_compare_Json:
        for compare_dic in target_compare_Json:
            compare_name = compare_dic["name"]
            if compare_name == name:
                if compare_dic.has_key("percentage"):
                    compare_per = compare_dic["percentage"]
                    perChangeStr = report_dic["percentage"] - compare_per
                    perChangeStr = "%.2f" % perChangeStr
                break

    single_crash_log = (
        str(i) + "\t" + name + "\t" + ("%.2f" % (report_dic["percentage"])) + "\t" + fileDirName + "\t" + perChangeStr)
    if CJFKit.validateString(max_controller_name):
        single_crash_log = (single_crash_log + "\t" + max_controller_name + "\n")
    else:
        single_crash_log = (single_crash_log + "\n")
    all_sort_result_reports_str += single_crash_log
    i += 1

out_file_name = target_input_filedir + "/sortOut/SortOutReports"
CJFKit.safeWriteFileContentStr(out_file_name, all_sort_result_reports_str)

print "Sort out is done"
print "result report is output in SortOutFinalResult"

timeEnd = time.time()
print "Program execution cost %f s" % (timeEnd - timeStart)
