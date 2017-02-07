# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    请使用命令: python JDiOSAllCrashConvertMutilProcess.py <iPad/iPhone> <fileDir>
    脚本将自动解析指定目录下的 *.json 文件,请将 KCrash上报的数据放置在里面.
    默认只解析 instruction_addr,如果需要同时解析 symbol_addr ,请将 target_need_symbol 常量置为 True .
    脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
    如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True

    崩溃解析格式文件内容:(四大数组格式不再变化)
    [
        {
            #崩溃文件全局性信息:
            system:{},
            crashOccurTime: localTime,
            bgTimeInterval: timeSpace,
            diagnosis: ...,
            error:{},
            crashThreadIndex: xx,
        },
        {
            崩溃线程信息
        },
        {
            崩溃额外信息
        },
        {
            崩溃用户行为信息
        }
    ]
"""

import collections
import glob
import json
import os
import sys
import time
import multiprocessing

import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False
target_need_cache = False
target_need_print = False

# 输入文件夹名字
target_input_filedir = None

# dsym文件名字,外部赋值
target_dsym_fileName = None

# app运行名,外部赋值,内部值最终是下面两者之一
target_app_run_name = None
global_appName_ipad = "Jdipad"
global_appName_iphone = "JD4iPhone"

# 合法的灰度版本号,仅iPhone支持,外部赋值
target_grayScale_flag = "Gray_560_PP2"

# 合法的app_uuid
target_app_uuid_list = []

# 后台bug,暂时修复,合法build和version校验,外部赋值
target_iPad_build_version = "8050"
target_iPad_build_short_version = "3.9.0"

target_iPhone_build_version = "5.5.0"
target_iPhone_build_short_version = "125580"

target_build_version = None #"8050" / "5.5.0"
target_build_short_version = None #"3.9.0" / "125580"

# 仅仅做文件分离操作
target_file_category_classify = False

# ============================== 非配置项 ==================
# 其文件无限复用
target_system_cache_name = "systemCache"

# 合法架构symbol文件,不需要多进程同步,简单的拷贝就好
target_symbol_fileDict = {}

# 全局用户信息
target_userinfo_dict = None

# 多线程相关变量
manager = multiprocessing.Manager()
# 需要附加的文件
needAppendVersion = manager.dict()
needAppendVersionLock = manager.Lock()

# 模糊映射文件
vagueMappingDict = manager.dict()
vagueMappingDictLock = manager.Lock()

# 全局缓存文件
symbolParseCache = manager.dict()
symbolParseCacheLock = manager.Lock()

target_symbol_cache_storage = "./cache"

# 全局支持架构字典
target_localSymbol_supportCPUList = []

# 全局关键字典
globalKeyWordDic = manager.dict()
globalKeyWordDicLock = manager.Lock()

# 全局crash uuid list
globalUUIDList = manager.list()
globalUUIDListLock = manager.Lock()

# 全局关键字
globalFileValidateCount = "globalFileValidateCount"
globalFileErrorCount = "globalFileErrorCount"

globalNormalCrashCount = "globalNormalCrashCount"
globalOtherCrashCount = "globalOtherCrashCount"
globalOOMCrashCountBG = "globalOOMCountBG"
globalOOMCrashCountAT = "globalOOMCountAT"
globalOOMCrashCountIA = "globalOOMCountIA"
globalOOMCrashCountFG = "globalOOMCountFG"
globalOOMCrashCountBL = "globalOOMCrashCountBL"
globalOOMCrashCountNone = "globalOOMCrashCountNone"

globalKeyWordDic[globalFileValidateCount] = 0
globalKeyWordDic[globalFileErrorCount] = 0
globalKeyWordDic[globalNormalCrashCount] = 0
globalKeyWordDic[globalOtherCrashCount] = 0
globalKeyWordDic[globalOOMCrashCountBG] = 0
globalKeyWordDic[globalOOMCrashCountAT] = 0
globalKeyWordDic[globalOOMCrashCountBL] = 0
globalKeyWordDic[globalOOMCrashCountIA] = 0
globalKeyWordDic[globalOOMCrashCountFG] = 0
globalKeyWordDic[globalOOMCrashCountNone] = 0


# -------------------------------  函数定义区 ----------------------------- #
# 全局关键字设置
def addGlobalUUIDListCount(value):
    global globalUUIDList
    global globalUUIDListLock
    globalUUIDListLock.acquire()
    globalUUIDList.append(value)
    globalUUIDListLock.release()


def addGlobalValueCount(keyValue, value):
    global globalKeyWordDic
    global globalKeyWordDicLock
    globalKeyWordDicLock.acquire()
    globalKeyWordDic[keyValue] = globalKeyWordDic[keyValue] + value
    globalKeyWordDicLock.release()


# 传入文件类型、基地址、符号地址 和 体系结构 即可解析
def parseCrashByAddress(originFileName, baseAddress, symbolAddress, archiver, isLocalSymbol):
    archiver = toValidateArchiver(archiver, isLocalSymbol)
    if not CJFKit.validateString(originFileName):
        return ""
    if not CJFKit.validateInteger(baseAddress):
        return ""
    if not CJFKit.validateInteger(symbolAddress):
        return ""
    if baseAddress <= 0 or symbolAddress <= 0:
        return ""

    cmd = (
        "atos -arch " + archiver + " -o %s -l " % originFileName + "0x%x" % baseAddress + " " + "0x%x" % symbolAddress)
    try:
        outStr = os.popen(cmd).read()
    except:
        return ""
    if CJFKit.validateString(outStr):
        return outStr
    else:
        return ""


# 合法化体系结构
def toValidateArchiver(archiver, isLocalSymbol):
    global target_localSymbol_supportCPUList
    if CJFKit.validateString(archiver):
        if archiver == "arm64" or archiver == "armv7" or archiver == "armv7s":
            if isLocalSymbol:
                if archiver in target_localSymbol_supportCPUList:
                    pass
                else:
                    if (archiver == "armv7s" or archiver == "armv7f") and (
                                "armv7" in target_localSymbol_supportCPUList):
                        archiver = "armv7"
                    else:
                        archiver = "arm64"
        else:
            archiver = "arm64"
    else:
        archiver = "arm64"
    return archiver


# 初始化符号文件映射表
def initSymbolFileMapping():
    global target_symbol_fileDict
    global target_localSymbol_supportCPUList
    global target_app_run_name
    global target_app_run_name

    target_symbol_fileDict = {target_app_run_name:"../SourceSymbol/self/" + target_dsym_fileName}

    # 本地app镜像路径初始化

    # 本地文件支持架构
    target_localSymbol_supportCPUList = []
    localFilePath = target_symbol_fileDict[target_app_run_name]
    cmd = ("lipo -info " + localFilePath)

    try:
        outStr = os.popen(cmd).read()
    except:
        print "Error: get Local Symbol file cpu support failed!"
        outStr = None
    if CJFKit.validateString(outStr):
        if "armv7" in outStr:
            target_localSymbol_supportCPUList.append("armv7")
        if "arm64" in outStr:
            target_localSymbol_supportCPUList.append("arm64")
        if "armv7s" in outStr:
            target_localSymbol_supportCPUList.append("armv7s")
        if "armv7f" in outStr:
            target_localSymbol_supportCPUList.append("armv7f")
    else:
        target_localSymbol_supportCPUList.append("armv7")
        target_localSymbol_supportCPUList.append("arm64")

    fileDirTuple = ("arm64", "armv7", "armv7s")
    # 系统镜像路径初始化
    for archiver in fileDirTuple:
        fileDict = {}
        symbolList = os.listdir("../SourceSymbol/" + archiver)
        for symbolFilePath in symbolList:
            if symbolFilePath != ".DS_Store":
                fileDict[symbolFilePath] = "../SourceSymbol/" + archiver + "/" + symbolFilePath
        target_symbol_fileDict[archiver] = fileDict


# 如果对应的文件不存在的话,将返回None,否则返回文件相对路径
# noinspection PyTypeChecker
def getSymbolFile(imageName, archiver, iosVersion):
    global target_symbol_fileDict
    global vagueMappingDict
    global vagueMappingDictLock

    if imageName == target_app_run_name:
        return CJFKit.safeGetDicElement(target_symbol_fileDict, target_app_run_name)

    fileName = imageName + "_" + iosVersion
    ret = CJFKit.safeGetElement(target_symbol_fileDict, [archiver, fileName])
    if CJFKit.validateString(ret):
        return ret

    # 开始模糊匹配
    vagueMappingName = imageName + "_" + iosVersion + "_" + archiver
    vagueMappingDictLock.acquire()
    if vagueMappingDict.has_key(vagueMappingName):
        ret = vagueMappingDict[vagueMappingName]
        vagueMappingDictLock.release()
        return ret
    else:
        # 对精简版性能优化
        if len(CJFKit.safeGetDicElement(target_symbol_fileDict, archiver)) == 0:
            vagueMappingDictLock.release()
            return None
        iosVersionList = iosVersion.split(".")
        if len(iosVersionList) == 2:
            for appendNumStr in "123":
                newVersionList = [iosVersionList[0], iosVersionList[1], appendNumStr]
                newVersionStr = ".".join(newVersionList)
                ret = CJFKit.safeGetElement(target_symbol_fileDict, [archiver, imageName + "_" + newVersionStr])
                if CJFKit.validateString(ret):
                    vagueMappingDict[vagueMappingName] = ret
                    vagueMappingDictLock.release()
                    return ret
        elif len(iosVersionList) == 3:
            appendNum = int(iosVersionList[-1])
            while appendNum >= 2:
                appendNumStr = str(appendNum - 1)
                newVersionList = [iosVersionList[0], iosVersionList[1], appendNumStr]
                newVersionStr = ".".join(newVersionList)
                ret = CJFKit.safeGetElement(target_symbol_fileDict, [archiver, imageName + "_" + newVersionStr])
                if CJFKit.validateString(ret):
                    vagueMappingDict[vagueMappingName] = ret
                    vagueMappingDictLock.release()
                    return ret
                appendNum -= 1

            appendNum = int(iosVersionList[-1])
            for stepNum in range(1, 4):
                appendNumStr = str(appendNum + stepNum)
                newVersionList = [iosVersionList[0], iosVersionList[1], appendNumStr]
                newVersionStr = ".".join(newVersionList)
                ret = CJFKit.safeGetElement(target_symbol_fileDict, [archiver, imageName + "_" + newVersionStr])
                if CJFKit.validateString(ret):
                    vagueMappingDict[vagueMappingName] = ret
                    vagueMappingDictLock.release()
                    return ret

            newVersionList = [iosVersionList[0], iosVersionList[1]]
            newVersionStr = ".".join(newVersionList)
            ret = CJFKit.safeGetElement(target_symbol_fileDict, [archiver, imageName + "_" + newVersionStr])
            if CJFKit.validateString(ret):
                vagueMappingDict[vagueMappingName] = ret
                vagueMappingDictLock.release()
                return ret
        else:
            vagueMappingDictLock.release()
            return None
        vagueMappingDictLock.release()
        return None


# 解析线程内容
def parserThreadSymbol(crashStackContent, arch, iosVersion):
    global target_app_run_name
    global needAppendVersion
    global needAppendVersionLock
    global symbolParseCache
    global symbolParseCacheLock
    crashSymbolList = []
    if CJFKit.validateList(crashStackContent) and CJFKit.validateString(arch) and CJFKit.validateString(iosVersion):
        for crashSingleSymbol in crashStackContent:
            try:
                object_addr = crashSingleSymbol["object_addr"]
                instruction_addr = crashSingleSymbol["instruction_addr"]
                object_name = crashSingleSymbol["object_name"]
                symbol_name = crashSingleSymbol["symbol_name"]
            except:
                continue

            symbolSourceFileName = None
            isLocalSymbol = False
            if CJFKit.validateString(object_name) and CJFKit.validateString(arch) and CJFKit.validateString(iosVersion):
                symbolSourceFileName = getSymbolFile(object_name, arch, iosVersion)
                if object_name == target_app_run_name:
                    isLocalSymbol = True
                else:
                    isLocalSymbol = False

            if CJFKit.validateString(symbolSourceFileName) and CJFKit.validateNumber(
                    object_addr) and CJFKit.validateNumber(instruction_addr):

                if isLocalSymbol:
                    symbolKey = symbolSourceFileName + "_" + str(
                            instruction_addr - object_addr) + "_" + toValidateArchiver(arch, True)
                else:
                    symbolKey = symbolSourceFileName + "_" + str(instruction_addr - object_addr)

                symbolParseCacheLock.acquire()
                if symbolParseCache.has_key(symbolKey):
                    crashSymbolList.append(symbolParseCache[symbolKey])
                    symbolParseCacheLock.release()
                else:
                    symbolParseCacheLock.release()
                    crashInstructionParser = parseCrashByAddress(symbolSourceFileName, object_addr, instruction_addr,
                                                                 arch, isLocalSymbol)
                    if CJFKit.validateString(crashInstructionParser):
                        if crashInstructionParser[-1] == "\n":
                            crashInstructionParser = crashInstructionParser[:-1]

                    if not crashInstructionParser:
                        crashSymbol = str(object_name) + (
                            "  0x%x  0x%x " % (int(object_addr), int(instruction_addr))) + CJFKit.toValidateString(
                                symbol_name)
                        crashSymbolList.append(crashSymbol)
                    else:
                        crashSymbolList.append(crashInstructionParser)
                        symbolParseCacheLock.acquire()
                        symbolParseCache[symbolKey] = crashInstructionParser
                        symbolParseCacheLock.release()
            else:
                # 尝试获取缓存
                if CJFKit.validateString(object_name) and CJFKit.validateNumber(
                        instruction_addr) and CJFKit.validateNumber(object_addr):
                    symbolKey = "../SourceSymbol/" + arch + "/" + object_name + "_" + iosVersion + "_" + str(
                            instruction_addr - object_addr)
                    symbolParseCacheLock.acquire()
                    if symbolParseCache.has_key(symbolKey):
                        crashSymbolList.append(symbolParseCache[symbolKey])
                        symbolParseCacheLock.release()
                        continue
                    else:
                        symbolParseCacheLock.release()

                # 不要隐藏无法翻译的符号
                crashSymbol = str(object_name) + (
                    "  0x%x  0x%x " % (int(object_addr), int(instruction_addr))) + CJFKit.toValidateString(symbol_name)
                crashSymbolList.append(crashSymbol)

                needAppendSymbolName = object_name + "_" + iosVersion + "_" + arch
                if not CJFKit.validateString(needAppendSymbolName):
                    continue
                needAppendVersionLock.acquire()
                # 符号化 instruction_addr
                if needAppendVersion.has_key(needAppendSymbolName):
                    needAppendVersion[needAppendSymbolName] += 1
                else:
                    needAppendVersion[needAppendSymbolName] = 1
                needAppendVersionLock.release()
    return crashSymbolList

def mutipleProcessMethod(inputFilePath):
    global target_input_filedir

    crashDic = CJFKit.safeGetFileContentJSON(inputFilePath)
    if not CJFKit.validateDictionary(crashDic):
        if target_need_print:
            print "Error: file %s json failed." % inputFilePath
        addGlobalValueCount(globalFileErrorCount, 1)
        return

    # 每解析一行，写入行号加1
    addGlobalValueCount(globalFileValidateCount, 1)

    # 在此处嵌入服务器返回的用户信息
    serverUserInfoDic = CJFKit.safeGetDicElement(target_userinfo_dict, os.path.basename(inputFilePath))
    if CJFKit.validateDictionary(serverUserInfoDic):
        crashDic["serverUserInfo"] = serverUserInfoDic
    else:
        crashDic["serverUserInfo"] = None

    # 全局需要使用的数据
    iosVersion = CJFKit.safeGetElement(crashDic, ["system", "system_version"])
    arch = CJFKit.safeGetElement(crashDic, ["system", "cpu_arch"])

    oomDic = CJFKit.safeGetElement(crashDic, ["essential_sys"])
    crashGrayScale = CJFKit.safeGetElement(crashDic, ["grayscaleFlag"])

    CFBundleVersion = CJFKit.safeGetElement(crashDic, ["system", "CFBundleVersion"])
    CFBundleShortVersionString = CJFKit.safeGetElement(crashDic, ["system", "CFBundleShortVersionString"])

    # 文件过滤器,优先 其他(模拟器、灰度过滤) -> OOM -> build+version过滤 -> normal crash
    if CJFKit.validateString(arch) and (arch == "x86" or arch == "i386"):
        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/other/" + os.path.basename(inputFilePath), crashDic)
        addGlobalValueCount(globalOtherCrashCount, 1)
        return

    # 灰度标识过滤
    if CJFKit.validateString(target_grayScale_flag) and crashGrayScale != target_grayScale_flag:
        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/other/" + os.path.basename(inputFilePath), crashDic)
        addGlobalValueCount(globalOtherCrashCount, 1)
        return
    else:
        pass

    if CJFKit.validateDictionary(oomDic):
        app_uuid = CJFKit.safeGetElement(crashDic, ["essential_sys", "app_uuid"])
    else:
        app_uuid = CJFKit.safeGetElement(crashDic, ["system", "app_uuid"])
    if CJFKit.validateString(app_uuid):
        if CJFKit.validateList(target_app_uuid_list):
            is_validate_app_uuid_flag = False
            for validate_app_uuid in target_app_uuid_list:
                if app_uuid == validate_app_uuid:
                    is_validate_app_uuid_flag = True
                    break
            if not is_validate_app_uuid_flag:
                CJFKit.safeWriteFileContentJSON(target_input_filedir + "/other/" + os.path.basename(inputFilePath),
                                                crashDic)
                addGlobalValueCount(globalOtherCrashCount, 1)
                return
        else:
            pass
    else:
        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/other/" + os.path.basename(inputFilePath), crashDic)
        addGlobalValueCount(globalOtherCrashCount, 1)
        return

    if CJFKit.validateDictionary(oomDic):
        app_event = CJFKit.safeGetElement(crashDic, ["event"])
        if CJFKit.validateList(app_event):
            app_event.reverse()
            for last_event_dic in app_event:
                last_event_action = CJFKit.safeGetDicElement(last_event_dic, "e")
                if CJFKit.validateString(last_event_action):
                    if last_event_action == "bg":
                        app_event.reverse()
                        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/BG/" + os.path.split(inputFilePath)[1],
                                                        crashDic)
                        addGlobalValueCount(globalOOMCrashCountBG, 1)
                        return
                    elif last_event_action == "fg":
                        app_event.reverse()
                        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/FG/" + os.path.split(inputFilePath)[1],
                                                        crashDic)
                        addGlobalValueCount(globalOOMCrashCountFG, 1)
                        return
                    elif last_event_action == "at":
                        app_event.reverse()
                        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/AT/" + os.path.split(inputFilePath)[1],
                                                        crashDic)
                        addGlobalValueCount(globalOOMCrashCountAT, 1)
                        return
                    elif last_event_action == "ia":
                        app_event.reverse()
                        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/IA/" + os.path.split(inputFilePath)[1],
                                                        crashDic)
                        addGlobalValueCount(globalOOMCrashCountIA, 1)
                        return
                    elif last_event_action == "bl":
                        app_event.reverse()
                        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/BL/" + os.path.split(inputFilePath)[1],
                                                        crashDic)
                        addGlobalValueCount(globalOOMCrashCountBL, 1)
                        return
            app_event.reverse()
        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/None/" + os.path.split(inputFilePath)[1], crashDic)
        addGlobalValueCount(globalOOMCrashCountNone, 1)
        return

    # 后台bug,非法Build和Version过滤
    if CFBundleVersion != target_build_version or CFBundleShortVersionString != target_build_short_version:
        CJFKit.safeWriteFileContentJSON(target_input_filedir + "/other/" + os.path.basename(inputFilePath), crashDic)
        addGlobalValueCount(globalOtherCrashCount, 1)
        return

    # 解析normal crash
    addGlobalValueCount(globalNormalCrashCount, 1)
    crashUUID = os.path.basename(inputFilePath).split("_")[0]
    addGlobalUUIDListCount(crashUUID)
    if target_file_category_classify:
        return
    if arch == "armv7f":
        arch = "armv7"

    # 头部信息提取
    system = CJFKit.safeGetElement(crashDic, ["system"])
    if CJFKit.validateDictionary(system):
        system["boot_time"] = CJFKit.UTCTimeStrToLocalTimeStr(system["boot_time"])
        system["app_start_time"] = CJFKit.UTCTimeStrToLocalTimeStr(system["app_start_time"])

    diagnosis = CJFKit.safeGetElement(crashDic, ["crash", "diagnosis"])
    process = CJFKit.safeGetElement(crashDic, ["process"])

    crashOccurTime = CJFKit.safeGetElement(crashDic, ["report", "timestamp"])
    crashOccurTime = CJFKit.UTCTimeStrToLocalTimeStr(crashOccurTime)

    error = CJFKit.safeGetElement(crashDic, ["crash", "error"])

    bgTimeInterval = None
    mwTimeInterval = None
    bgFindFinished = False

    userInfo = CJFKit.safeGetDicElement(crashDic, "user")
    if CJFKit.validateDictionary(userInfo):
        app_event = CJFKit.safeGetElement(userInfo, ["event_history"])
        if CJFKit.validateList(app_event):
            app_event.reverse()
            for last_event_dic in app_event:
                if bgFindFinished and mwTimeInterval:
                    break
                last_event_action = CJFKit.safeGetDicElement(last_event_dic, "e")
                if CJFKit.validateString(last_event_action):
                    if not bgFindFinished:
                        if last_event_action == "bg":
                            bgTimeBegin = CJFKit.safeGetDateObjFormStr(CJFKit.safeGetDicElement(last_event_dic, "t"))
                            crashTimeBegin = CJFKit.safeGetDateObjFormStr(crashOccurTime)
                            bgTimeInterval = CJFKit.getTimeInterval(crashTimeBegin, bgTimeBegin)
                            bgFindFinished = True
                        elif last_event_action == "at" or last_event_action == "fg" or last_event_action == "ia":
                            bgFindFinished = True
                    if (not mwTimeInterval) and last_event_action == "mw":
                        mwTimeBegin = CJFKit.safeGetDateObjFormStr(CJFKit.safeGetDicElement(last_event_dic, "t"))
                        crashTimeBegin = CJFKit.safeGetDateObjFormStr(crashOccurTime)
                        mwTimeInterval = CJFKit.getTimeInterval(crashTimeBegin, mwTimeBegin)
            app_event.reverse()

    # 规范化数据
    if isinstance(bgTimeInterval, float) and bgTimeInterval < 0:
        bgTimeInterval = None
    if isinstance(mwTimeInterval, float) and mwTimeInterval < 0:
        mwTimeInterval = None

    crashThreadIndex = None
    notableAddress = None
    crashThreadSymbolList = None
    mainThreadSymbolList = None
    AllThreadData = CJFKit.safeGetElement(crashDic, ["crash", "threads"])
    if isinstance(AllThreadData, collections.Iterable):
        for threadData in AllThreadData:
            crashThreadFlag = CJFKit.safeGetDicElement(threadData, "crashed")
            threadIndex = CJFKit.safeGetDicElement(threadData, "index")
            if (isinstance(crashThreadFlag, bool) and crashThreadFlag) or threadIndex == 0:
                crashStackContent = CJFKit.safeGetElement(threadData, ["backtrace", "contents"])
                if isinstance(crashThreadFlag, bool) and crashThreadFlag:
                    crashThreadIndex = threadIndex
                    notableAddress = CJFKit.safeGetDicElement(threadData, "notable_addresses")
                    crashThreadSymbolList = parserThreadSymbol(crashStackContent, arch, iosVersion)
                else:
                    mainThreadSymbolList = parserThreadSymbol(crashStackContent, arch, iosVersion)
                if (isinstance(crashThreadFlag, bool) and crashThreadFlag) and threadIndex == 0:
                    break
                if isinstance(crashThreadSymbolList, list) and isinstance(mainThreadSymbolList, list):
                    break

    # 使用list来帮助dict排序,因为dict本身是无序的
    outputArr = []
    outputDic1 = {}
    outputDic2 = {}
    outputDic3 = {}
    outputDic4 = {}

    # 崩溃文件全局性信息:
    outputDic1["system"] = system
    outputDic1["crashOccurTime"] = crashOccurTime
    outputDic1["mwTimeInterval"] = mwTimeInterval
    outputDic1["bgTimeInterval"] = bgTimeInterval
    outputDic1["diagnosis"] = diagnosis
    outputDic1["error"] = error
    outputDic1["crashThreadIndex"] = crashThreadIndex

    # 崩溃文件线程信息
    outputDic2["process"] = process
    outputDic2["crashThreadSymbolList"] = crashThreadSymbolList
    if isinstance(mainThreadSymbolList, list):
        outputDic2["mainThreadSymbolList"] = mainThreadSymbolList

    # 崩溃文件额外信息
    outputDic3["notableAddress"] = notableAddress

    # 崩溃文件用户信息
    outputDic4["user"] = userInfo
    outputDic4["serverUserInfo"] = crashDic["serverUserInfo"]

    outputArr.append(outputDic1)
    outputArr.append(outputDic2)
    outputArr.append(outputDic3)
    outputArr.append(outputDic4)

    crashData = json.dumps(outputArr, indent = 4)
    outputFileName = target_input_filedir + "/parser/" + os.path.split(inputFilePath)[1]
    try:
        writerFileFP = open(outputFileName, "w")
        writerFileFP.write(crashData)
    except:
        print "Error: writer file %s error." % outputFileName
    finally:
        writerFileFP.close()


# ----------------------------------  正式代码区域 -------------------------------------- #

timeStart = time.time()
# iPhone/iPad  target_dir_relative_path  version  build  dsym_file_name
if not target_debug_flag:
    if len(sys.argv) >= 7:
        appName = sys.argv[1]
        target_input_filedir = sys.argv[2]
        # 由于iPhone的build和version是反的,所以需要反转
        if appName == "iPhone":
            target_app_run_name = global_appName_iphone
            target_build_short_version = sys.argv[4]
            target_build_version = sys.argv[3]
        else:
            target_app_run_name = global_appName_ipad
            target_build_short_version = sys.argv[3]
            target_build_version = sys.argv[4]

        target_dsym_fileName = sys.argv[5]
        sys_need_cache = sys.argv[6]
        if sys_need_cache == "0":
            target_need_cache = False
        else:
            target_need_cache = True
        if len(sys.argv) >= 8:
            target_grayScale_flag = sys.argv[7]
        else:
            target_grayScale_flag = ""
    else:
        print "Error: need origin fileDir Param. Please use : python iOSCrashParser.py <iPad/iPhone> <fileDir>"
        sys.exit(-1)
else:
    target_app_run_name = "Jdipad"
    target_iPad_build_short_version = "3.9.0"
    target_iPad_build_version = "8050"
    target_input_filedir = "../testtest/iPad_390_1125"
    target_dsym_fileName = "Jdipad"
    target_grayScale_flag = ""
    target_need_cache = True

    target_app_run_name = "JD4iPhone"
    target_iPad_build_short_version = "3.9.0"
    target_iPad_build_version = "8050"
    target_input_filedir = "../testtest/iPad_390_1125"
    target_dsym_fileName = "Jdipad"
    target_grayScale_flag = ""
    target_need_cache = True

# 初始化映射表文件
initSymbolFileMapping()

# 初始化jd symbol缓存文件,不启用本地缓存
if target_need_cache:
    if target_app_run_name == global_appName_ipad:
        symbol_cache_fileName = target_dsym_fileName + "_" + target_iPad_build_short_version + "_" + target_iPad_build_version
    else:
        symbol_cache_fileName = target_dsym_fileName + "_" + target_iPhone_build_short_version + "_" + target_iPhone_build_version
    symbol_cache_filePath = target_symbol_cache_storage + "/" + symbol_cache_fileName
    if os.path.isfile(symbol_cache_filePath):
        symbol_cache_local_data = CJFKit.safeGetFileContentJSON(symbol_cache_filePath)
        if CJFKit.validateDictionary(symbol_cache_local_data):
            for key in symbol_cache_local_data.keys():
                symbolParseCache[key] = symbol_cache_local_data[key]

# 初始化system symbol缓存文件
system_cache_filePath = target_symbol_cache_storage + "/" + target_system_cache_name
if os.path.isfile(system_cache_filePath):
    system_cache_local_data = CJFKit.safeGetFileContentJSON(system_cache_filePath)
    if CJFKit.validateDictionary(system_cache_local_data):
        for key in system_cache_local_data.keys():
            symbolParseCache[key] = system_cache_local_data[key]

# 初始化用户映射表
if os.path.isfile(target_input_filedir + "/userInfoMapping.json"):
    target_userinfo_dict = CJFKit.safeGetFileContentJSON(target_input_filedir + "/userInfoMapping.json")

if not CJFKit.validateDictionary(target_userinfo_dict):
    target_userinfo_dict = None

# 删除之前的输出文件
CJFKit.safeRemovePath(target_input_filedir + "/ConvertResult")
# 新建解析文件夹
CJFKit.safeClearDir(target_input_filedir + "/parser")
# 新建其他文件夹
CJFKit.safeClearDir(target_input_filedir + "/other")
# 新建OOM文件夹
CJFKit.safeClearDir(target_input_filedir + "/oom")
os.mkdir(target_input_filedir + "/oom/BG")
os.mkdir(target_input_filedir + "/oom/FG")
os.mkdir(target_input_filedir + "/oom/IA")
os.mkdir(target_input_filedir + "/oom/AT")
os.mkdir(target_input_filedir + "/oom/BL")
os.mkdir(target_input_filedir + "/oom/None")

crashFileName = target_input_filedir + "/source/*.json"
crashFileList = glob.glob(crashFileName)
if CJFKit.validateList(crashFileList):
    pass
else:
    print "Error: need crash file in %s , file name style like *.json ." % target_input_filedir
    sys.exit(-1)

runPool = multiprocessing.Pool()
# 支持多文件解析
for inputFile in crashFileList:
    runPool.apply_async(mutipleProcessMethod, args = (inputFile,))

print "Waiting for all subprocesses done...\n"
runPool.close()
runPool.join()
print "All subprocesses done.\n"

# symbol文件持久化
print "will do symbol && system cache storage.\n"
# 由于 manager.dict()是 dictproxy ,无法被json化,因此需要做类型转换操作
symbol_cache_local_data = {}
system_cache_local_data = {}
for key in symbolParseCache.keys():
    if target_app_run_name in key:
        symbol_cache_local_data[key] = symbolParseCache[key]
    else:
        system_cache_local_data[key] = symbolParseCache[key]
CJFKit.safeCreateDir(target_symbol_cache_storage)

if target_need_cache:
    CJFKit.safeWriteFileContentJSON(symbol_cache_filePath, symbol_cache_local_data)
    print "symbol cache storage is finish, file path : %s \n" % symbol_cache_filePath

CJFKit.safeWriteFileContentJSON(system_cache_filePath, system_cache_local_data)
print "system cache storage is finish, file path : %s \n" % system_cache_filePath

allCrashFileCount = len(crashFileList)
allCrashFileCount = allCrashFileCount - globalKeyWordDic[globalOtherCrashCount]

successCrashFileCount = globalKeyWordDic[globalFileValidateCount] - globalKeyWordDic[globalOtherCrashCount]

uuidSet = set(globalUUIDList)

# 打印以及输出汇总信息
needVersionStr = "#######################  Parser Report  #######################\n"
needVersionStr += "Parser crash data all count : %d \n" % allCrashFileCount
if allCrashFileCount > 0:
    needVersionStr += "Parser crash success count : %d percentage: %.2f%% \n" % (
        successCrashFileCount, successCrashFileCount * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash Other crash count : %d \n" % (globalKeyWordDic[globalOtherCrashCount])
    needVersionStr += "Parser crash data error count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalFileErrorCount], globalKeyWordDic[globalFileErrorCount] * 100.0 / allCrashFileCount)

    needVersionStr += "\nParser crash data normal crash count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalNormalCrashCount], globalKeyWordDic[globalNormalCrashCount] * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash uniqueness count : %d \n" % (len(uuidSet))
    needVersionStr += "Parser crash data oom IA count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalOOMCrashCountIA], globalKeyWordDic[globalOOMCrashCountIA] * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash data oom AT count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalOOMCrashCountAT], globalKeyWordDic[globalOOMCrashCountAT] * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash data oom FG count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalOOMCrashCountFG], globalKeyWordDic[globalOOMCrashCountFG] * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash data oom BG count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalOOMCrashCountBG], globalKeyWordDic[globalOOMCrashCountBG] * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash data oom BG count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalOOMCrashCountBL], globalKeyWordDic[globalOOMCrashCountBL] * 100.0 / allCrashFileCount)
    needVersionStr += "Parser crash data oom None count : %d percentage: %.2f%% \n" % (
        globalKeyWordDic[globalOOMCrashCountNone],
        globalKeyWordDic[globalOOMCrashCountNone] * 100.0 / allCrashFileCount)

needVersionStr += "\nneed code version : \n"
needVersionStr += json.dumps(dict(needAppendVersion), indent = 4)
needVersionStr += "\n\ncode vague mapping : \n"
needVersionStr += json.dumps(dict(vagueMappingDict), indent = 4)
needVersionStr += "\n################################################################"

resultOutputFileName = target_input_filedir + "/ConvertResult"
open(resultOutputFileName, "w").write(needVersionStr)
print needVersionStr

print "Parser is done"
print "result report is output in ConvertResult"

timeEnd = time.time()
print "Program execution cost %f s" % (timeEnd - timeStart)
