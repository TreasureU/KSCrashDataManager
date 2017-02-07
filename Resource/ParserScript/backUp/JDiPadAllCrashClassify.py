# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
	请使用命令: python xxipadAllCrashClassify.py <iPad/iPhone> <fileDir>
	脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.
	脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
	如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import os, glob, sys, json
import ParserScript.CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False

# 关键字映射文件
global_crash_keyword_mapping_iPadfileName = "./setting/crashKeyWordMappingiPad.json"
global_crash_keyword_mapping_iPhonefileName = "./setting/crashKeyWordMappingiPhone.json"
target_crash_keyword_mapping_fileName = None

global_crash_keyword_mapping = None

# 关键功能参数表
# 子文件夹按照controller排列,并输出单独的报告
classifyByController = "classifyByController"


# ----------------------------------  函数定义区 --------------------------------------- #

def safeSymbolLinkCrashFile(fileName, dstName):
    global target_input_filedir
    fileName = target_input_filedir + "/parser/" + fileName
    ParserScript.CJFKit.safeSymbolLink(fileName, dstName)


def classifyByControllerMethod(fileName, dirName, fileJson):
    global target_input_filedir
    global classifyByController
    last_nav_history = ParserScript.CJFKit.safeGetElement(fileJson, [-1, "user", "nav_history", -1, "c"])
    if not ParserScript.CJFKit.validateString(last_nav_history):
        last_nav_history = "None"
    if not os.path.isdir(
                                            target_input_filedir + "/classify/" + dirName + "/" + last_nav_history):
        os.mkdir(target_input_filedir + "/classify/" + dirName + "/" + last_nav_history)
    if singleParamReportDic[classifyByController + "_" + dirName].has_key(last_nav_history):
        singleParamReportDic[classifyByController + "_" + dirName][last_nav_history] += 1
    else:
        singleParamReportDic[classifyByController + "_" + dirName][last_nav_history] = 1
    outputFileName = target_input_filedir + "/classify/" + dirName + "/" + last_nav_history + "/" + os.path.basename(
        fileName)
    safeSymbolLinkCrashFile(os.path.basename(fileName), outputFileName)


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
    target_input_filedir = "../2016_0807"

if os.path.isfile(target_crash_keyword_mapping_fileName):
    global_crash_keyword_mapping = ParserScript.CJFKit.safeGetFileContentJSON(target_crash_keyword_mapping_fileName,
                                                                              True)

if not ParserScript.CJFKit.validateList(global_crash_keyword_mapping):
    print "Error: global_crash_keyword_mapping build error."
    sys.exit(-1)

# 新建分类文件夹
ParserScript.CJFKit.safeClearDir(target_input_filedir + "/classify")

singleParamReportDic = {}

# 初始化分类文件夹
for searchPair in global_crash_keyword_mapping:
    searchPairDirName = ParserScript.CJFKit.safeGetDicElement(searchPair, "fileDirName")
    searchPairParam = ParserScript.CJFKit.safeGetDicElement(searchPair, "param")
    if ParserScript.CJFKit.validateString(searchPairDirName):
        if not os.path.isdir(target_input_filedir + "/classify/" + searchPairDirName):
            os.makedirs(target_input_filedir + "/classify/" + searchPairDirName)
        if searchPairParam and ParserScript.CJFKit.safeGetDicElement(searchPairParam, classifyByController):
            singleParamReportDic[classifyByController + "_" + searchPairDirName] = {}

if not os.path.isdir(target_input_filedir + "/classify/" + "not_mached"):
    os.makedirs(target_input_filedir + "/classify/" + "not_mached")

if not os.path.isdir(target_input_filedir + "/classify/" + "BG"):
    os.makedirs(target_input_filedir + "/classify/" + "BG")

file_error_count = 0
file_error_list = []
file_bg_count = 0
needClassifyFileList = glob.glob(target_input_filedir + "/parser/*.json")
allFileCount = len(needClassifyFileList)
if allFileCount <= 0:
    print "Warning: %s/parser is no *.json file" % target_input_filedir
    sys.exit(-1)

for needClassifyFileName in needClassifyFileList:
    needClassifyFileStr = ParserScript.CJFKit.safeGetFileContentStr(needClassifyFileName, True)
    if not ParserScript.CJFKit.validateString(needClassifyFileStr):
        print "Error: file %s content is empty." % needClassifyFileName
        file_error_count = file_error_count + 1
        file_error_list.append(needClassifyFileName)
        continue

    try:
        needClassifyFileJson = json.loads(needClassifyFileStr)
    except:
        print "Error: file %s json decode is error." % needClassifyFileName
        file_error_count = file_error_count + 1
        file_error_list.append(needClassifyFileName)
        continue

    last_event_history = ParserScript.CJFKit.safeGetElement(needClassifyFileJson,
                                                            [-1, "user", "event_history", -1, "e"])
    if ParserScript.CJFKit.validateString(last_event_history) and last_event_history == "bg":
        file_bg_count = file_bg_count + 1
        outputFileName = target_input_filedir + "/classify/BG/" + os.path.basename(needClassifyFileName)
        safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName)
        continue

    for searchPair in global_crash_keyword_mapping:
        searchPairDirName = ParserScript.CJFKit.safeGetDicElement(searchPair, "fileDirName")
        searchPairKeyWord = ParserScript.CJFKit.safeGetDicElement(searchPair, "keyWord")
        searchPairKeyWords = ParserScript.CJFKit.safeGetDicElement(searchPair, "keyWords")
        searchPairParam = ParserScript.CJFKit.safeGetDicElement(searchPair, "param")
        if ParserScript.CJFKit.validateString(searchPairDirName) and ParserScript.CJFKit.validateString(
                searchPairKeyWord):
            # 校验是否符合情况
            if searchPairKeyWord in needClassifyFileStr:
                if searchPair.has_key("count"):
                    searchPair["count"] = searchPair["count"] + 1
                else:
                    searchPair["count"] = 1

                # 附加参数处理区
                if searchPairParam and ParserScript.CJFKit.safeGetDicElement(searchPairParam, classifyByController):
                    classifyByControllerMethod(needClassifyFileName, searchPairDirName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/classify/" + searchPairDirName + "/" + os.path.basename(
                        needClassifyFileName)
                    safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName)
                break
        elif ParserScript.CJFKit.validateString(searchPairDirName) and ParserScript.CJFKit.validateList(
                searchPairKeyWords):
            # 校验是否符合情况
            findCount = 0
            for needFindKey in searchPairKeyWords:
                if needFindKey in needClassifyFileStr:
                    findCount += 1
            if findCount == len(searchPairKeyWords):
                if searchPair.has_key("count"):
                    searchPair["count"] = searchPair["count"] + 1
                else:
                    searchPair["count"] = 1
                # 附加参数处理区
                if searchPairParam and ParserScript.CJFKit.safeGetDicElement(searchPairParam, classifyByController):
                    classifyByControllerMethod(needClassifyFileName, searchPairDirName, needClassifyFileJson)
                else:
                    outputFileName = target_input_filedir + "/classify/" + searchPairDirName + "/" + os.path.basename(
                        needClassifyFileName)
                    safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName)
                break
    else:
        # 直接写入未匹配文件夹
        outputFileName = target_input_filedir + "/classify/not_mached/" + os.path.basename(needClassifyFileName)
        safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName)

allMatchCount = 0
for searchPair in global_crash_keyword_mapping:
    if not searchPair.has_key("count"):
        searchPair["count"] = 0
        searchPair["perCentage"] = 0
    else:
        allMatchCount = allMatchCount + searchPair["count"]
        selfCount = searchPair["count"] * 100.0
        searchPair["perCentage"] = selfCount / allFileCount

noMatchDic = {"fileDirName":"not_mached", "keyWord":None,
              "count":(allFileCount - file_error_count - file_bg_count - allMatchCount),
              "perCentage":((allFileCount - file_error_count - file_bg_count - allMatchCount) * 100.0 / allFileCount)}
allFileDic = {"fileDirName":"all_file", "keyWord":None, "count":allFileCount,
              "perCentage":100.0}
bgFileDic = {"fileDirName":"bg_file", "keyWord":"last event is : bg", "count":file_bg_count,
             "perCentage":(file_bg_count * 100.0 / allFileCount)}
errorFileDic = {"fileDirName":"error_file", "keyWord":None, "count":file_error_count,
                "perCentage":(file_error_count * 100.0 / allFileCount)}
global_crash_keyword_mapping.append(noMatchDic)
global_crash_keyword_mapping.append(allFileDic)
global_crash_keyword_mapping.append(bgFileDic)
global_crash_keyword_mapping.append(errorFileDic)

# 统一数据排序
global_crash_keyword_mapping.sort(key = lambda x:x["perCentage"], reverse = True)

for classifyByControllerKey in singleParamReportDic:
    if ParserScript.CJFKit.validateString(classifyByControllerKey) and classifyByControllerKey.find(
            classifyByController) >= 0:
        classifyByControllerDic = singleParamReportDic[classifyByControllerKey]
        classifyByControllerArr = []
        for allControllerKey in classifyByControllerDic:
            tmpDic = {"controllerName":allControllerKey, "count":classifyByControllerDic[allControllerKey]}
            classifyByControllerArr.append(tmpDic)
        classifyByControllerArr.sort(key = lambda x:x["count"], reverse = True)
        ParserScript.CJFKit.safeWriteFileContentJSON(
            target_input_filedir + "/ClassifyResult_" + classifyByControllerKey,
            classifyByControllerArr, True,
            True)

global_crash_keyword_mapping.append({"error_file_list":file_error_list})
ParserScript.CJFKit.safeWriteFileContentJSON(target_input_filedir + "/ClassifyResult", global_crash_keyword_mapping,
                                             True, True)

print "Classify is done"
print "result report is output in ClassifyResult"
