# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    请使用命令: python JDiOSCrashSortOutInit.py <iPad/iPhone> <fileDir>
    脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.
    脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
    如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
    归类依据:
        1.先判断 crashThread 中有无归属于 xxipad 的类信息,有的话,那么就按照这个输出分配。
        2.再判断 userInfo 中的最后一个页面归属于何方
        3.输出整体报表.
    注意:在 not_sort 中也会包含 crash_controller 的信息,但不参与计数工作
"""

import glob
import json
import os
import sys
import time

import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False
target_remove_bg = True

# 后台筛选时间
target_bg_limit = 10.0

global_iPad_name = "xxipad"
global_iPhone_name = "xxxiPhone"

global_keyword_iPad_fileName = "./setting/filterKeyWordMappingiPad.json"
global_keyword_iPhone_fileName = "./setting/filterKeyWordMappingiPhone.json"
target_crash_keyword_mapping_fileName = None

global_crash_keyword_mapping = {}
global_crash_Mapping_list = []

# assit数据统计
# 操作系统数据统计
global_osVersionDict = {}
# 设备类型统计
global_deviceTypeDict = {}
# 平均active时间计算
global_active_timeCount = 0.0
global_background_timeCount = 0.0

# 关键功能参数表
# 子文件夹按照controller排列,并输出单独的报告
classifyByController = "classifyByController"


# ----------------------------------  函数定义区 --------------------------------------- #

def safeSymbolLinkCrashFile(fileName, dstName, dirName = "../.."):
    fileName = dirName + "/parser/" + fileName
    CJFKit.safeSymbolLink(fileName, dstName)


def classifyByControllerMethod(compareModel, fileName, fileJson):
    global target_input_filedir
    global classifyByController
    local_last_nav_history = CJFKit.safeGetElement(fileJson, [-1, "user", "nav_history", -1, "c"])
    if not CJFKit.validateString(local_last_nav_history):
        local_last_nav_history = "None"
    CJFKit.safeCreateDir(
            target_input_filedir + "/sortOut/crash_symbol/" + compareModel.fileDirName + "/" + local_last_nav_history)
    compareModel.addController(local_last_nav_history)
    local_outputFileName = target_input_filedir + "/sortOut/crash_symbol/" + compareModel.fileDirName + "/" + local_last_nav_history + "/" + os.path.basename(
            fileName)
    safeSymbolLinkCrashFile(os.path.basename(fileName), local_outputFileName, "../../../..")


def addOsVersionCount(osVersionName):
    if global_osVersionDict.has_key(osVersionName):
        global_osVersionDict[osVersionName] += 1
    else:
        global_osVersionDict[osVersionName] = 1


def addDeviceTypeCount(local_deviceType):
    if global_deviceTypeDict.has_key(local_deviceType):
        global_deviceTypeDict[local_deviceType] += 1
    else:
        global_deviceTypeDict[local_deviceType] = 1


def computeRealTime(userEventList, crashTime):
    if not CJFKit.validateList(userEventList):
        return None
    activeAllTimeCount = 0.0
    atTime = None
    iaTime = None
    for appEventDic in userEventList:
        eventName = CJFKit.safeGetDicElement(appEventDic, "e")
        if eventName == "at":
            atTime = CJFKit.safeGetDicElement(appEventDic, "t")
        if eventName == "ia":
            iaTime = CJFKit.safeGetDicElement(appEventDic, "t")
        if atTime and iaTime:
            session_active_time = CJFKit.getTimeIntervalByStr(iaTime, atTime)
            atTime = None
            iaTime = None
            if session_active_time:
                activeAllTimeCount += session_active_time

    if atTime and iaTime is None:
        iaTime = crashTime
        session_active_time = CJFKit.getTimeIntervalByStr(iaTime, atTime)
        if session_active_time:
            activeAllTimeCount += session_active_time

    return activeAllTimeCount


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
            target_crash_keyword_mapping_fileName = global_keyword_iPhone_fileName
        else:
            target_name = global_iPad_name
            target_crash_keyword_mapping_fileName = global_keyword_iPad_fileName
        target_input_filedir = sys.argv[2]
    else:
        print "Error: need origin fileDir Param. Please use : python xxipadCrashParser.py <fileDir>"
        sys.exit(-1)
else:
    target_name = global_iPad_name
    target_crash_keyword_mapping_fileName = global_keyword_iPad_fileName
    target_input_filedir = "../iPad_390_1125"

# 新建分类文件夹
CJFKit.safeClearDir(target_input_filedir + "/sortOut")
CJFKit.safeCreateDir(target_input_filedir + "/sortOut/" + "crash_symbol")
CJFKit.safeCreateDir(target_input_filedir + "/sortOut/" + "crash_controller")
CJFKit.safeCreateDir(target_input_filedir + "/sortOut/" + "crash_system")
CJFKit.safeCreateDir(target_input_filedir + "/sortOut/" + "not_sortOut")

# 初始化切换表
if os.path.isfile(target_crash_keyword_mapping_fileName):
    global_crash_keyword_mapping = CJFKit.safeGetFileContentJSON(target_crash_keyword_mapping_fileName, True)

if not CJFKit.validateList(global_crash_keyword_mapping):
    print "Error: global_crash_keyword_mapping build error."
    sys.exit(-1)

singleParamReportDic = {}
# 初始化分类文件夹
for searchPair in global_crash_keyword_mapping:
    tmpModel = CJFKit.systemCrashModel.dictToSystemCrashModel(searchPair)
    if tmpModel:
        global_crash_Mapping_list.append(tmpModel)

crash_file_dic = {}

file_error_count = 0
file_error_list = []

file_symbol_count = 0
file_symbol_dic = {}

file_controller_count = 0
file_controller_dic = {}

file_not_sortOut_count = 0

# 后台crash先一步去除
if target_remove_bg:
    file_bg_count = 0
    CJFKit.safeCreateDir(target_input_filedir + "/sortOut/" + "BG")

needClassifyFileList = glob.glob(target_input_filedir + "/parser/*.json")
allFileCount = len(needClassifyFileList)
if allFileCount <= 0:
    print "Warning: %s/parser is no *.json file" % target_input_filedir
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

    # assitInfo数据获取
    osVersion = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "system_version"])
    if not osVersion:
        osVersion = "None"
    addOsVersionCount(osVersion)

    deviceType = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "machine"])
    if not deviceType:
        deviceType = "None"
    addDeviceTypeCount(deviceType)

    activeTimeSinceLaunch = 0
    if target_name == global_iPhone_name:
        # app_start_time = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "app_start_time"])
        # crashOccurTime = CJFKit.safeGetElement(needClassifyFileJson, [0, "crashOccurTime"])
        # activeTimeSinceLaunch = CJFKit.getTimeIntervalByStr(crashOccurTime,app_start_time)
        # if not activeTimeSinceLaunch:
        # 	activeTimeSinceLaunch = 0
        activeTimeSinceLaunch = computeRealTime(
            CJFKit.safeGetElement(needClassifyFileJson, [-1, "user", "event_history"]),
            CJFKit.safeGetElement(needClassifyFileJson, [0, "crashOccurTime"]))
        if CJFKit.validateNumber(activeTimeSinceLaunch):
            if activeTimeSinceLaunch < 0:
                activeTimeSinceLaunch = 0
        else:
            activeTimeSinceLaunch = 0
        application_stats = CJFKit.safeGetElement(needClassifyFileJson, [0, "system", "application_stats"])
        if CJFKit.validateDictionary(application_stats):
            application_stats["active_time_since_launch"] = activeTimeSinceLaunch
    else:
        activeTimeSinceLaunch = CJFKit.safeGetElement(needClassifyFileJson,
                                                      [0, "system", "application_stats", "active_time_since_launch"])
        if not CJFKit.validateNumber(activeTimeSinceLaunch):
            activeTimeSinceLaunch = 0.0
        elif activeTimeSinceLaunch < 0:
            activeTimeSinceLaunch = 0.0

    global_active_timeCount += activeTimeSinceLaunch

    bgTimeSinceLaunch = CJFKit.safeGetElement(needClassifyFileJson,
                                              [0, "system", "application_stats", "background_time_since_launch"])
    if not CJFKit.validateNumber(bgTimeSinceLaunch):
        bgTimeSinceLaunch = 0.0
    elif bgTimeSinceLaunch < 0.0:
        bgTimeSinceLaunch = 0.0
    global_background_timeCount += bgTimeSinceLaunch

    if target_remove_bg:
        bgTimeInterval = CJFKit.safeGetElement(needClassifyFileJson, [0, "bgTimeInterval"])
        if bgTimeInterval is not None and target_bg_limit > bgTimeInterval > 0:
            file_bg_count += 1
            outputFileName = target_input_filedir + "/sortOut/BG/" + os.path.basename(needClassifyFileName)
            safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName)
            continue

    needContinue = False
    # Possible zombie
    diagnosis = CJFKit.safeGetElement(needClassifyFileJson, [0, "diagnosis"])
    if CJFKit.validateString(diagnosis) and diagnosis.find("Possible zombie in call:") >= 0:
        crash_symbol_index = diagnosis.find("\n")
        if crash_symbol_index > 0:
            crashSymbol = diagnosis[0:crash_symbol_index]
            fileDirName = None
            if file_symbol_dic.has_key(crashSymbol):
                file_symbol_dic[crashSymbol].count += 1
            else:
                model = CJFKit.systemCrashModel(crashSymbol, ("%d" % len(file_symbol_dic)))
                model.count += 1
                file_symbol_dic[crashSymbol] = model
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_symbol/" + model.fileDirName)
            # fileDirName = file_symbol_dic[crashSymbol].fileDirName
            # outputName = target_input_filedir + "/sortOut/crash_symbol/" + fileDirName + "/" + os.path.basename(
            #     needClassifyFileName)
            # safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputName, "../../..")
            systemCompareModel = file_symbol_dic[crashSymbol]
            if isinstance(systemCompareModel.controllers, dict):
                classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
            else:
                outputFileName = target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName + "/" + os.path.basename(
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
            needContinue = True

    if needContinue:
        file_symbol_count += 1
        continue

    # 前置关键字匹配
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
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName)
                # 附加参数处理区
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName + "/" + os.path.basename(
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
                needContinue = True
                break

        # 匹配到使用单一关键字的情况
        elif CJFKit.validateString(systemCompareModel.fileDirName) and CJFKit.validateString(
                systemCompareModel.keyWord):
            # 校验是否符合情况
            if systemCompareModel.keyWord in needClassifyFileStr:
                systemCompareModel.count += 1
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName)
                # 附加参数处理区
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName + "/" + os.path.basename(
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
                needContinue = True
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
                CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName)
                # 附加参数处理区
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName + "/" + os.path.basename(
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
                needContinue = True
                break

    if needContinue:
        file_symbol_count += 1
        continue

    # symbol crash归类
    crashThreadSymbolList = CJFKit.safeGetElement(needClassifyFileJson, [1, "crashThreadSymbolList"])
    if CJFKit.validateList(crashThreadSymbolList):
        for crashSymbol in crashThreadSymbolList:
            if CJFKit.validateString(crashSymbol) and (target_name in crashSymbol) and (not ("main" in crashSymbol)):
                fileDirName = None
                if file_symbol_dic.has_key(crashSymbol):
                    file_symbol_dic[crashSymbol].count += 1
                else:
                    model = CJFKit.systemCrashModel(crashSymbol, ("%d" % len(file_symbol_dic)))
                    model.count += 1
                    file_symbol_dic[crashSymbol] = model
                    CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_symbol/" + model.fileDirName)
                # fileDirName = file_symbol_dic[crashSymbol].fileDirName
                # outputName = target_input_filedir + "/sortOut/crash_symbol/" + fileDirName + "/" + os.path.basename(needClassifyFileName)
                # safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName),outputName,"../../..")
                # 附加参数处理区
                systemCompareModel = file_symbol_dic[crashSymbol]
                if isinstance(systemCompareModel.controllers, dict):
                    classifyByControllerMethod(systemCompareModel, needClassifyFileName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/sortOut/crash_symbol/" + systemCompareModel.fileDirName + "/" + os.path.basename(
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
                needContinue = True
                break

    if needContinue:
        file_symbol_count += 1
        continue

    # 页面归类
    last_nav_history = CJFKit.safeGetElement(needClassifyFileJson, [-1, "user", "nav_history", -1, "c"])
    if CJFKit.validateString(last_nav_history):
        if file_controller_dic.has_key(last_nav_history):
            file_controller_dic[last_nav_history].count += 1
        else:
            model = CJFKit.systemCrashModel(last_nav_history, last_nav_history)
            model.count += 1
            file_controller_dic[last_nav_history] = model
            CJFKit.safeCreateDir(target_input_filedir + "/sortOut/crash_controller/" + model.fileDirName)
        fileDirName = file_controller_dic[last_nav_history].fileDirName
        outputName = target_input_filedir + "/sortOut/crash_controller/" + fileDirName + "/" + os.path.basename(
                needClassifyFileName)
        safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputName, "../../..")

        outputName = target_input_filedir + "/sortOut/not_sortOut/" + os.path.basename(needClassifyFileName)
        safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputName, "../..")
        needContinue = True

    if needContinue:
        file_controller_count += 1
        continue

    # 未归类事件安放
    outputName = target_input_filedir + "/sortOut/not_sortOut/" + os.path.basename(needClassifyFileName)
    safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputName, "../..")
    file_not_sortOut_count += 1

# 所有解析出来的数据排序
file_symbol_list = []
for sortModelKey in file_symbol_dic:
    sortModel = file_symbol_dic[sortModelKey]
    sortModel.percentage = sortModel.count * 100.0 / allFileCount
    tmpSortDic = sortModel.convertToSymbolDict()
    file_symbol_list.append(tmpSortDic)

for tmpModel in global_crash_Mapping_list:
    # 输出全部报告的地方
    tmpModel.percentage = tmpModel.count * 100.0 / allFileCount
    file_symbol_list.append(tmpModel.convertToDict())

file_symbol_list.sort(key = lambda x:x["count"], reverse = True)

# controller分类数据排序
file_controller_list = []
for sortModelKey in file_controller_dic:
    sortModel = file_controller_dic[sortModelKey]
    sortModel.percentage = sortModel.count * 100.0 / allFileCount
    tmpSortDic = {"name":sortModel.description, "fileDirName":sortModel.fileDirName, "count":sortModel.count,
                  "percentage":sortModel.percentage}
    file_controller_list.append(tmpSortDic)
file_controller_list.sort(key = lambda x:x["count"], reverse = True)

# 所有解析结果概览
symbol_result_dic = {"name":"paired symbol crash result",
                     "count":file_symbol_count,
                     "percentage":(file_symbol_count * 100.0 / allFileCount)}
controller_result_dic = {"name":"paired controller name crash result",
                         "count":file_controller_count,
                         "percentage":(file_controller_count * 100.0 / allFileCount)}
if target_remove_bg:
    bg_result_dic = {"name":"BG crash result",
                     "count":file_bg_count,
                     "percentage":(file_bg_count * 100.0 / allFileCount)}
noMatch_result_dic = {"name":"no match crash result",
                      "count":file_not_sortOut_count,
                      "percentage":(file_not_sortOut_count * 100.0 / allFileCount)}
error_result_dic = {"name":"file error result",
                    "count":file_error_count,
                    "percentage":(file_error_count * 100.0 / allFileCount)}
all_result_dic = {"name":"all result",
                  "count":allFileCount,
                  "percentage":100.0}

result_list = [all_result_dic,
               symbol_result_dic,
               controller_result_dic,
               noMatch_result_dic,
               error_result_dic]

if target_remove_bg:
    result_list.append(bg_result_dic)

symbol_crash_subController = {}
for symbol_model_key in file_symbol_dic.keys():
    symbol_model = file_symbol_dic[symbol_model_key]
    CJFKit.safeWriteFileContentJSON(
            target_input_filedir + "/sortOut/crash_symbol/" + symbol_model.fileDirName + "/assitInfo",
            symbol_model.getCrashAssitInfo())
    symbol_crash_subController[symbol_model.description] = symbol_model.controllers

for symbol_model in global_crash_Mapping_list:
    CJFKit.safeWriteFileContentJSON(
            target_input_filedir + "/sortOut/crash_symbol/" + symbol_model.fileDirName + "/assitInfo",
            symbol_model.getCrashAssitInfo())
    symbol_crash_subController[symbol_model.description] = symbol_model.controllers

# 最终输出拼接
out_put_result_list = [
    {
        "result glance":result_list
    },
    {
        "symbol crash sort result":file_symbol_list
    },
    {
        "symbol crash controller sort result":symbol_crash_subController
    },
    {
        "controller crash sort result":file_controller_list
    },
    {
        "file error list":file_error_list
    }
]

assitInfoDict = {"osVersionSort":CJFKit.systemCrashModel.getSortListFormDict(global_osVersionDict),
                 "deviceTypeSort":CJFKit.systemCrashModel.getSortListFormDict(global_deviceTypeDict)}

timeCostCountDic = {"global_active_timeCount":global_active_timeCount * 1.0 / allFileCount,
                    "global_background_timeCount":global_background_timeCount * 1.0 / allFileCount}
timeCostCountDic["global_launch_timeCount"] = timeCostCountDic["global_active_timeCount"] + timeCostCountDic[
    "global_background_timeCount"]

assitInfoDict["timeCostCount"] = timeCostCountDic

CJFKit.safeWriteFileContentJSON(target_input_filedir + "/sortOut/assitInfo", assitInfoDict)

out_file_name = target_input_filedir + "/sortOut/SortOutInitResult"
CJFKit.safeWriteFileContentJSON(out_file_name, out_put_result_list)

print "Sort out is done"
print "result report is output in SortOutInitResult"

timeEnd = time.time()
print "Program execution cost %f s" % (timeEnd - timeStart)
