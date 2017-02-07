# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
	注意,本文件暂未兼容iPhone,且不再更新与维护。
	请使用命令: python xxipadAllCrashConvert.py <fileDir>
	脚本将自动解析同一目录下的 *.json 文件,请将 KCrash上报的数据放置在里面.
	默认只解析 instruction_addr,如果需要同时解析 symbol_addr ,请将 target_need_symbol 常量置为 True .
	脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
	如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import sys, os, glob, json, time, collections
import ParserScript.CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False

# 需要同时解析symbol
target_need_symbol = False

# app运行名
target_app_run_name = "xxipad"

# 合法架构symbol文件
target_symbol_fileDict = {}

# 需要附加的文件
needAppendVersion = {}

# 模糊映射文件
vagueMappingDict = {}


# -------------------------------  函数定义区 ----------------------------- #


# 传入文件类型、基地址、符号地址 和 体系结构 即可解析
def parseCrashByAddress(originFileName, baseAddress, symbolAddress, archiver, isLocalSymbol):
    archiver = toValidateArchiver(archiver, isLocalSymbol)

    if not ParserScript.CJFKit.validateString(originFileName):
        return ""
    if not ParserScript.CJFKit.validateInteger(baseAddress):
        return ""
    if not ParserScript.CJFKit.validateInteger(symbolAddress):
        return ""
    if baseAddress <= 0 or symbolAddress <= 0:
        return ""

    cmd = ("atos -arch " + archiver + " -o %s -l " % originFileName
           + "0x%x" % baseAddress + " " + "0x%x" % symbolAddress)
    outStr = os.popen(cmd).read()
    if ParserScript.CJFKit.validateString(outStr):
        return outStr
    else:
        return ""


# 合法化体系结构
def toValidateArchiver(archiver, isLocalSymbol):
    if ParserScript.CJFKit.validateString(archiver):
        if archiver == "arm64" or archiver == "armv7" or archiver == "armv7s":
            if isLocalSymbol and archiver == "armv7s":
                archiver = "armv7"
        else:
            archiver = "arm64"
    else:
        archiver = "arm64"
    return archiver


# 初始化符号文件映射表
def initSymbolFileMapping():
    global target_symbol_fileDict
    target_symbol_fileDict = {}
    target_symbol_fileDict[target_app_run_name] = "../SourceSymbol/xxipad/xxipad"
    fileDirTuple = ("arm64", "armv7", "armv7s")
    for archiver in fileDirTuple:
        fileDict = {}
        symbolList = os.listdir("../SourceSymbol/" + archiver)
        for symbolFilePath in symbolList:
            if symbolFilePath != ".DS_Store":
                fileDict[symbolFilePath] = "../SourceSymbol/" + archiver + "/" + symbolFilePath
        target_symbol_fileDict[archiver] = fileDict


# 如果对应的文件不存在的话,将返回None,否则返回文件相对路径
def getSymbolFile(imageName, archiver, iosVersion):
    global target_symbol_fileDict
    global vagueMappingDict
    ret = None
    if imageName == target_app_run_name:
        return ParserScript.CJFKit.safeGetDicElement(target_symbol_fileDict, target_app_run_name)
    fileName = imageName + "_" + iosVersion
    ret = ParserScript.CJFKit.safeGetElement(target_symbol_fileDict, [archiver, fileName])
    if ParserScript.CJFKit.validateString(ret):
        return ret

    # 开始模糊匹配
    vagueMappingName = imageName + "_" + iosVersion + "_" + archiver
    if vagueMappingDict.has_key(vagueMappingName):
        return vagueMappingDict[vagueMappingName]
    else:
        iosVersionList = iosVersion.split(".")
        if len(iosVersionList) == 2:
            for appendNumStr in "123":
                newVersionList = [iosVersionList[0], iosVersionList[1], appendNumStr]
                newVersionStr = ".".join(newVersionList)
                ret = ParserScript.CJFKit.safeGetElement(target_symbol_fileDict,
                                                         [archiver, imageName + "_" + newVersionStr])
                if ParserScript.CJFKit.validateString(ret):
                    vagueMappingDict[vagueMappingName] = ret
                    return ret
        elif len(iosVersionList) == 3:
            appendNum = int(iosVersionList[-1])
            while appendNum >= 2:
                appendNumStr = str(appendNum - 1)
                newVersionList = [iosVersionList[0], iosVersionList[1], appendNumStr]
                newVersionStr = ".".join(newVersionList)
                ret = ParserScript.CJFKit.safeGetElement(target_symbol_fileDict,
                                                         [archiver, imageName + "_" + newVersionStr])
                if ParserScript.CJFKit.validateString(ret):
                    vagueMappingDict[vagueMappingName] = ret
                    return ret
                appendNum = appendNum - 1

            appendNum = int(iosVersionList[-1])
            for stepNum in range(1, 4):
                appendNumStr = str(appendNum + stepNum)
                newVersionList = [iosVersionList[0], iosVersionList[1], appendNumStr]
                newVersionStr = ".".join(newVersionList)
                ret = ParserScript.CJFKit.safeGetElement(target_symbol_fileDict,
                                                         [archiver, imageName + "_" + newVersionStr])
                if ParserScript.CJFKit.validateString(ret):
                    vagueMappingDict[vagueMappingName] = ret
                    return ret

            newVersionList = [iosVersionList[0], iosVersionList[1]]
            newVersionStr = ".".join(newVersionList)
            ret = ParserScript.CJFKit.safeGetElement(target_symbol_fileDict,
                                                     [archiver, imageName + "_" + newVersionStr])
            if ParserScript.CJFKit.validateString(ret):
                vagueMappingDict[vagueMappingName] = ret
                return ret
        else:
            return None
        return None


# 解析线程内容
def parserThreadSymbol(crashStackContent, arch, iosVersion):
    global needAppendVersion
    global target_app_run_name
    crashSymbolList = []
    if ParserScript.CJFKit.validateList(crashStackContent) and ParserScript.CJFKit.validateString(
            arch) and ParserScript.CJFKit.validateString(iosVersion):
        for crashSingleSymbol in crashStackContent:
            object_addr = 0
            instruction_addr = 0
            symbol_addr = 0
            object_name = ""
            try:
                object_addr = crashSingleSymbol["object_addr"]
                instruction_addr = crashSingleSymbol["instruction_addr"]
                symbol_addr = crashSingleSymbol["symbol_addr"]
                object_name = crashSingleSymbol["object_name"]
            except:
                print "inputFile %s key error : crashSingleSymbol get error ." % inputFile
                continue

            symbolSourceFileName = None
            isLocalSymbol = False
            if ParserScript.CJFKit.validateString(object_name):
                symbolSourceFileName = getSymbolFile(object_name, arch, iosVersion)
                if object_name == target_app_run_name:
                    isLocalSymbol = True
                else:
                    isLocalSymbol = False

            if ParserScript.CJFKit.validateString(symbolSourceFileName):
                # 符号化 symbol_addr, 需要 常量开关打开方可解析
                if target_need_symbol:
                    crashSymbolParser = parseCrashByAddress(symbolSourceFileName, object_addr, instruction_addr,
                                                            arch, isLocalSymbol)
                    if ParserScript.CJFKit.validateString(crashSymbolParser):
                        crashSymbolList.append(crashSymbolParser)

                # 符号化 instruction_addr
                crashInstructionParser = parseCrashByAddress(symbolSourceFileName, object_addr, instruction_addr,
                                                             arch, isLocalSymbol)
                if ParserScript.CJFKit.validateString(crashInstructionParser):
                    crashSymbolList.append(crashInstructionParser)
            else:
                # 不要隐藏无法翻译的符号
                crashSymbol = str(object_name) + "  0x%x  0x%x" % (int(object_addr), int(instruction_addr))
                crashSymbolList.append(crashSymbol)

                needAppendSymbolName = object_name + "_" + iosVersion + "_" + arch
                if not ParserScript.CJFKit.validateString(needAppendSymbolName):
                    continue

                # 符号化 instruction_addr
                if needAppendVersion.has_key(needAppendSymbolName):
                    needAppendVersion[needAppendSymbolName] = needAppendVersion[needAppendSymbolName] + 1
                else:
                    needAppendVersion[needAppendSymbolName] = 1
    return crashSymbolList


# ----------------------------------  正式代码区域 -------------------------------------- #

timeStart = time.time()
print "Process is starting in %f ." % timeStart

# 初始化映射表文件
initSymbolFileMapping()

if not target_debug_flag:
    if len(sys.argv) >= 2:
        target_input_filedir = sys.argv[1]
    else:
        print "Error: need origin fileDir Param. Please use : python xxipadCrashParser.py <fileDir>"
        sys.exit(-1)
else:
    target_input_filedir = "../2016_07_01_13_35_52_674"

crashFileName = target_input_filedir + "/source/*.json"
crashFileList = glob.glob(crashFileName)
if ParserScript.CJFKit.validateList(crashFileList):
    pass
else:
    print "Error: need crash file in %s , file name style lick *.json ." % (target_input_filedir)
    sys.exit(-1)

# 输出表 CrashLog 中写入行号，每解析一行，写入行号加1
rowIndex = 0
crashOriginDataError = 0

# 支持多文件解析
for inputFile in crashFileList:

    try:
        crashFo = open(inputFile, "r+")
    except:
        print "Error: open file %s error. " % inputFile
        crashFo.close()
        crashOriginDataError += 1
        continue

    try:
        crashData = crashFo.read()
    except:
        print "Error: open file %s error." % inputFile
        crashFo.close()
        crashOriginDataError += 1
        continue

    crashFo.close()
    if not ParserScript.CJFKit.validateString(crashData):
        print "Error: file %s content is empty." % inputFile
        crashOriginDataError += 1
        continue

    try:
        # 注意,json解析后,所有的 str类型都转换为了 Unicode类型
        crashDic = json.loads(crashData)
    except:
        print "Error: operation file %s error." % inputFile
        crashOriginDataError += 1
        continue

    if not ParserScript.CJFKit.validateDictionary(crashDic):
        print "Error: file %s json decode failed." % inputFile
        crashOriginDataError += 1
        continue

    # 每解析一行，写入行号加1
    rowIndex += 1

    # 需要获取的数据
    iosVersion = ParserScript.CJFKit.safeGetElement(crashDic, ["system", "system_version"])
    arch = ParserScript.CJFKit.safeGetElement(crashDic, ["system", "cpu_arch"])
    if arch == "armv7f":
        print "%s is armv7f" % (inputFile)
        arch = "armv7"
    applicationActive = ParserScript.CJFKit.safeGetElement(crashDic,
                                                           ["system", "application_stats", "application_active"])
    applicationInForeground = ParserScript.CJFKit.safeGetElement(crashDic,
                                                                 ["system", "application_stats",
                                                                  "application_in_foreground"])

    selfImageAddress = None
    uikitImageAddress = None
    coreFoundationImageAddress = None
    libobjcImageAddress = None
    allImgLoadAddress = ParserScript.CJFKit.safeGetElement(crashDic, ["binary_images"])
    if ParserScript.CJFKit.validateList(allImgLoadAddress):
        for imageObj in allImgLoadAddress:
            image_name = ParserScript.CJFKit.safeGetDicElement(imageObj, "name")
            if ParserScript.CJFKit.validateString(image_name):
                if image_name.endswith("/xxipad"):
                    selfImageAddress = ParserScript.CJFKit.safeGetDicElement(imageObj, "image_addr")
                    selfImageAddress = "0x%x" % (int(selfImageAddress))
                elif image_name.endswith("/UIKit"):
                    uikitImageAddress = ParserScript.CJFKit.safeGetDicElement(imageObj, "image_addr")
                    uikitImageAddress = "0x%x" % (int(uikitImageAddress))
                elif image_name.endswith("/CoreFoundation"):
                    coreFoundationImageAddress = ParserScript.CJFKit.safeGetDicElement(imageObj, "image_addr")
                    coreFoundationImageAddress = "0x%x" % (int(coreFoundationImageAddress))
                elif image_name.endswith("/libobjc.A.dylib"):
                    libobjcImageAddress = ParserScript.CJFKit.safeGetDicElement(imageObj, "image_addr")
                    libobjcImageAddress = "0x%x" % (int(libobjcImageAddress))

    diagnosis = ParserScript.CJFKit.safeGetElement(crashDic, ["crash", "diagnosis"])
    process = ParserScript.CJFKit.safeGetElement(crashDic, ["process"])

    crashThreadIndex = None
    notableAddress = None
    crashThreadSymbolList = None
    mainThreadSymbolList = None
    AllThreadData = ParserScript.CJFKit.safeGetElement(crashDic, ["crash", "threads"])
    if isinstance(AllThreadData, collections.Iterable):
        for threadData in AllThreadData:
            crashThreadFlag = ParserScript.CJFKit.safeGetDicElement(threadData, "crashed")
            threadIndex = ParserScript.CJFKit.safeGetDicElement(threadData, "index")
            if (isinstance(crashThreadFlag, bool) and crashThreadFlag) or threadIndex == 0:
                crashStackContent = ParserScript.CJFKit.safeGetElement(threadData, ["backtrace", "contents"])
                if (isinstance(crashThreadFlag, bool) and crashThreadFlag):
                    crashThreadIndex = threadIndex
                    notableAddress = ParserScript.CJFKit.safeGetDicElement(threadData, "notable_addresses")
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

    outputDic1["iosVersion"] = iosVersion
    outputDic1["arch"] = arch
    outputDic1["applicationActive"] = applicationActive
    outputDic1["applicationInForeground"] = applicationInForeground
    outputDic1["selfImageAddress"] = selfImageAddress
    outputDic1["uikitImageAddress"] = uikitImageAddress
    outputDic1["coreFoundationImageAddress"] = coreFoundationImageAddress
    outputDic1["libobjcImageAddress"] = libobjcImageAddress
    outputDic1["crashThreadIndex"] = crashThreadIndex
    outputDic1["diagnosis"] = diagnosis

    outputDic2["process"] = process
    outputDic2["crashThreadSymbolList"] = crashThreadSymbolList
    if isinstance(mainThreadSymbolList, list):
        outputDic2["mainThreadSymbolList"] = mainThreadSymbolList

    outputDic3["notableAddress"] = notableAddress

    outputArr.append(outputDic1)
    outputArr.append(outputDic2)
    outputArr.append(outputDic3)

    crashData = json.dumps(outputArr, indent = 4)

    inputFileNameSplitList = inputFile.split("/")
    outputFileName = target_input_filedir + "/parser/" + inputFileNameSplitList[-1]
    open(outputFileName, "w").write(crashData)

# 打印以及输出汇总信息
needVersionStr = "#######################  Parser Report  #######################\n"
needVersionStr = needVersionStr + ("Parser crash success count : %d \n" % (rowIndex))
needVersionStr = needVersionStr + ("Parser crash data error count : %d \n" % crashOriginDataError)
needVersionStr = needVersionStr + ("need code version : \n")
needVersionStr = needVersionStr + json.dumps(needAppendVersion, indent = 4)
needVersionStr = needVersionStr + ("\ncode vague mapping : \n")
needVersionStr = needVersionStr + json.dumps(vagueMappingDict, indent = 4)
needVersionStr = needVersionStr + "\n################################################################"

resultOutputFileName = target_input_filedir + "/ConvertResult"
open(resultOutputFileName, "w").write(needVersionStr)

print needVersionStr

timeEnd = time.time()
print "Process is ending in %f ." % timeEnd
print "Program execution cost %f s" % (timeEnd - timeStart)
