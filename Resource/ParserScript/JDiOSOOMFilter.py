# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #


"""
说明区:
    快捷的OOM过滤
"""

import glob
import json
import sys

import CJFKit


# 全局调试宏
target_debug_flag = False

target_app_run_name = None
target_input_filedir = None

global_appName_iphone = "iPhone"
global_appName_ipad = "iPad"

globalNormalCrashCount = "globalNormalCrashCount"
globalAllOOMCrashCount = "globalAllOOMCrashCount"
globalOOMCrashCountBG = "globalOOMCountBG"
globalOOMCrashCountAT = "globalOOMCountAT"
globalOOMCrashCountIA = "globalOOMCountIA"
globalOOMCrashCountFG = "globalOOMCountFG"
globalOOMCrashCountBL = "globalOOMCrashCountBL"
globalOOMCrashCountNone = "globalOOMCrashCountNone"
globalErrorCrashCount = "globalErrorCrashCount"

target_count_dic = {
    globalNormalCrashCount:0,
    globalAllOOMCrashCount:0,
    globalOOMCrashCountBG:0,
    globalOOMCrashCountAT:0,
    globalOOMCrashCountIA:0,
    globalOOMCrashCountFG:0,
    globalOOMCrashCountBL:0,
    globalOOMCrashCountNone:0,
    globalErrorCrashCount:0
}

if not target_debug_flag:
    if len(sys.argv) >= 3:
        appName = sys.argv[1]
        if appName == "iPhone":
            target_app_run_name = global_appName_iphone
        else:
            target_app_run_name = global_appName_ipad
        target_input_filedir = sys.argv[2]
    else:
        print "Error: need origin fileDir Param. Please use : python JDiPadCrashParser.py <iPad/iPhone> <fileDir>"
        sys.exit(-1)
else:
    target_app_run_name = global_appName_ipad
    target_input_filedir = "../iPad_390_1125"

crashFileName = target_input_filedir + "/source/*.json"
crashFileList = glob.glob(crashFileName)
if CJFKit.validateList(crashFileList):
    pass
else:
    print "Error: need crash file in %s , file name style lick *.json ." % target_input_filedir
    sys.exit(-1)

globalAllCrashCount = len(crashFileList)

# 支持多文件解析
for inputFileName in crashFileList:
    crashStr = CJFKit.safeGetFileContentStr(inputFileName, True)
    if not CJFKit.validateString(crashStr):
        print "Error: file %s content is empty." % inputFileName
        target_count_dic[globalErrorCrashCount] += 1
        continue

    try:
        crashDic = json.loads(crashStr)
    except:
        print "Error: file %s json decode is error." % inputFileName
        target_count_dic[globalErrorCrashCount] += 1
        continue

    oomDic = CJFKit.safeGetElement(crashDic, ["essential_sys"])
    if CJFKit.validateDictionary(oomDic):
        target_count_dic[globalAllOOMCrashCount] += 1
        app_event = CJFKit.safeGetElement(crashDic, ["event"])
        if CJFKit.validateList(app_event):
            app_event.reverse()
            for last_event_dic in app_event:
                last_event_action = CJFKit.safeGetDicElement(last_event_dic, "e")
                if CJFKit.validateString(last_event_action):
                    if last_event_action == "bg":
                        target_count_dic[globalOOMCrashCountBG] += 1
                        break
                    elif last_event_action == "fg":
                        target_count_dic[globalOOMCrashCountFG] += 1
                        break
                    elif last_event_action == "at":
                        target_count_dic[globalOOMCrashCountAT] += 1
                        break
                    elif last_event_action == "ia":
                        target_count_dic[globalOOMCrashCountIA] += 1
                        break
                    elif last_event_action == "bl":
                        target_count_dic[globalOOMCrashCountBL] += 1
                        break
            else:
                target_count_dic[globalOOMCrashCountNone] += 1
        else:
            target_count_dic[globalOOMCrashCountNone] += 1
    else:
        target_count_dic[globalNormalCrashCount] += 1

needVersionStr = "#######################  Quick Statistics Report  #######################\n"
needVersionStr += "Quick Statistics  all count : %d \n" % globalAllCrashCount
if globalAllCrashCount > 0:

    needVersionStr += (
        "\nParser crash data normal crash count : %d percentage: %.2f%% \n" % (
            target_count_dic[globalNormalCrashCount],
            target_count_dic[globalNormalCrashCount] * 100.0 / globalAllCrashCount))

    needVersionStr += "Parser crash data error count : %d percentage: %.2f%% \n\n" % (
        target_count_dic[globalErrorCrashCount],
        target_count_dic[globalErrorCrashCount] * 100.0 / globalAllCrashCount)

    needVersionStr += "Parser crash data oom IA count : %d percentage: %.2f%% \n" % (
        target_count_dic[globalOOMCrashCountIA],
        target_count_dic[globalOOMCrashCountIA] * 100.0 / globalAllCrashCount)

    needVersionStr += "Parser crash data oom AT count : %d percentage: %.2f%% \n" % (
        target_count_dic[globalOOMCrashCountAT],
        target_count_dic[globalOOMCrashCountAT] * 100.0 / globalAllCrashCount)

    needVersionStr += "Parser crash data oom FG count : %d percentage: %.2f%% \n" % (
        target_count_dic[globalOOMCrashCountFG],
        target_count_dic[globalOOMCrashCountFG] * 100.0 / globalAllCrashCount)

    needVersionStr += "Parser crash data oom BG count : %d percentage: %.2f%% \n" % (
        target_count_dic[globalOOMCrashCountBG],
        target_count_dic[globalOOMCrashCountBG] * 100.0 / globalAllCrashCount)

    needVersionStr += "Parser crash data oom BG count : %d percentage: %.2f%% \n" % (
        target_count_dic[globalOOMCrashCountBL],
        target_count_dic[globalOOMCrashCountBL] * 100.0 / globalAllCrashCount)

    needVersionStr += "Parser crash data oom None count : %d percentage: %.2f%% \n" % (
        target_count_dic[globalOOMCrashCountNone],
        target_count_dic[globalOOMCrashCountNone] * 100.0 / globalAllCrashCount)

print needVersionStr
