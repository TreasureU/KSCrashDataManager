# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
	请使用命令: python JDiPadCrashParser.py <iPad/iPhone> <sourceDir> [appendName]
	脚本将自动解析指定目录下的 source/*.json 文件,请将 KCrash上报的数据放置在里面.
	<appendName> 表示输出文件附加命名,输出文件格式名为: JDiPadCrashPaser_20xx_xx_xx_<appendName>.xlsx
	默认只解析 instruction_addr,如果需要同时解析 symbol_addr ,请将 target_need_symbol 常量置为 True
	如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import xlsxwriter, sys, os, glob, time, json, CJFKit


# ----------------------------------  常量定义区域 -------------------------------------- #

# 全局调试宏,暂时未使用到
target_debug_flag = False

# symbol file path
target_symbol_file = None
global_symbol_ipad_file = "../SourceSymbol/Jdipad/Jdipad"
global_symbol_iphone_file = "../SourceSymbol/JD4iPhone/JD4iPhone"

# app运行名
target_app_run_name = None
global_appName_ipad = "Jdipad"
global_appName_iphone = "JD4iPhone"

# 需要同时解析symbol
target_need_symbol = False

# 附加名字
target_append_name = "3.7.0"

# 源文件夹
target_source_file = ""

# 设备输出表列表字段索引
typeColumnIndex = 0                 # 崩溃类型输出
reasonColumnIndex = 1               # 崩溃原因输出
crashThreadIndexColumnIndex = 2     # crash线程index
crashFileColumnIndex = 3            # crash文件名称
crashSymbolColumnIndex = 4          # crash线程symbol+instruction
crashRegisterInfoColumnIndex = 5    # crash线程寄存器信息
jailbrokenColumnIndex = 6           # 越狱标志
deviceTypeColumnIndex = 7           # 设备类型
osVersionColumnIndex = 8            # 系统版本
backgroundColumnIndex = 9           # 是否后台
useMemoryColumnIndex = 10           # 使用内存大小
unuseMemoryColumnIndex = 11         # 可用内存大小
memoryPerCountIndex = 12            # 内存占用百分比
deviceAppHashCountIndex = 13        # 设备hash标识
appStartTimeCountIndex = 14         # 设备启动时间


# -------------------------------  函数定义区 ----------------------------- #


# 传入文件类型、基地址、符号地址 和 体系结构 即可解析
def parseCrashByAddress(baseAddress, symbolAddress, archiver = "arm64"):
    if not CJFKit.validateInteger(baseAddress):
        return ""
    if not CJFKit.validateInteger(symbolAddress):
        return ""
    if baseAddress <= 0 or symbolAddress <= 0:
        return ""

    if CJFKit.validateString(archiver) and archiver == "arm64":
        pass
    else:
        archiver = "armv7"

    cmd = ("atos -arch " + archiver + " -o %s -l " % target_symbol_file
           + "0x%x" % baseAddress + " " + "0x%x" % symbolAddress)
    outStr = os.popen(cmd).read()
    if CJFKit.validateString(outStr):
        return outStr
    else:
        return ""


# ----------------------------------  正式代码区域 -------------------------------------- #

if not target_debug_flag:
    if len(sys.argv) >= 3:
        appName = sys.argv[1]
        if appName == "iPhone":
            target_app_run_name = global_appName_iphone
            target_symbol_file = global_symbol_iphone_file
        else:
            target_app_run_name = global_appName_ipad
            target_symbol_file = global_symbol_ipad_file
        target_source_file = sys.argv[2]
        if len(sys.argv) >= 4:
            target_append_name = sys.argv[3]
    else:
        print "Error: Please use cmd like : python JDiPadCrashParser.py <iPad/iPhone> sourceFileDir <appendName>"
        sys.exit(-1)
else:
    target_symbol_file = global_symbol_ipad_file
    target_app_run_name = global_appName_ipad
    target_source_file = "../2016_07_01_13_35_52_674"

# 校验有效文件
if not os.path.isfile(target_symbol_file):
    print "Error: need origin file in the dir , like %s" % target_symbol_file
    sys.exit(-1)

crashFileList = glob.glob(target_source_file + "/source/*.json")
if CJFKit.validateList(crashFileList):
    pass
else:
    print "Error: need crash file in the dir , file name style lick *.json ."
    sys.exit(-1)

# 创建输出表
todayTime = time.localtime()
outFilePath = target_app_run_name + (
"CrashPaser_%04d%02d%02d_%s.xlsx" % (todayTime[0], todayTime[1], todayTime[2], target_append_name))
outFilePath = target_source_file + "/" + outFilePath

# 先删除同名文件
if os.path.isfile(outFilePath):
    os.remove(outFilePath)

# 创建相关的 excel 文件
outFile = xlsxwriter.Workbook(outFilePath)
outTable = outFile.add_worksheet('CrashLog')
outCountTable = outFile.add_worksheet('CountResult')

# 输出格式创建,目前专注于使用xlsx
titleStyle1 = outFile.add_format({'border':1, 'align':'center', 'bg_color':'green', 'font_size':13, 'bold':True})
titleStyle2 = outFile.add_format({'border':1, 'align':'center', 'bg_color':'blue', 'font_size':13, 'bold':True})
contentCenterStyle = outFile.add_format({'align':'center', 'font_size':12})
contentLeftStyle = outFile.add_format({'font_size':12})
contentLightStyle = outFile.add_format({'align':'center', 'bg_color':'yellow', 'font_size':12})

outTable.set_column(typeColumnIndex, typeColumnIndex, 30)
outTable.set_column(reasonColumnIndex, reasonColumnIndex, 30)
outTable.set_column(crashThreadIndexColumnIndex, crashThreadIndexColumnIndex, 10)
outTable.set_column(crashFileColumnIndex, crashFileColumnIndex, 60)
outTable.set_column(crashSymbolColumnIndex, crashSymbolColumnIndex, 50)
outTable.set_column(crashRegisterInfoColumnIndex, crashRegisterInfoColumnIndex, 35)
outTable.set_column(jailbrokenColumnIndex, memoryPerCountIndex, 15)
outTable.set_column(deviceAppHashCountIndex, deviceAppHashCountIndex, 50)
outTable.set_column(appStartTimeCountIndex, appStartTimeCountIndex, 25)

outCountTable.set_column(0, 0, 90)
outCountTable.set_column(1, 1, 10)
outCountTable.set_column(2, 2, 20)

# 设置输出表 CrashLog 列表字段title
outTable.write_string(0, typeColumnIndex, "type", titleStyle1)
outTable.write_string(0, reasonColumnIndex, "reason", titleStyle2)
outTable.write_string(0, crashThreadIndexColumnIndex, "index", titleStyle1)
outTable.write_string(0, crashFileColumnIndex, "crashFileName", titleStyle2)
outTable.write_string(0, crashSymbolColumnIndex, "crashSymbol", titleStyle1)
outTable.write_string(0, crashRegisterInfoColumnIndex, "crashRegisterInfo", titleStyle2)
outTable.write_string(0, jailbrokenColumnIndex, "jailbroken", titleStyle1)
outTable.write_string(0, deviceTypeColumnIndex, "devcieType", titleStyle2)
outTable.write_string(0, osVersionColumnIndex, "osVersion", titleStyle1)
outTable.write_string(0, backgroundColumnIndex, "background", titleStyle2)
outTable.write_string(0, useMemoryColumnIndex, "useMemory", titleStyle1)
outTable.write_string(0, unuseMemoryColumnIndex, "unuseMemory", titleStyle2)
outTable.write_string(0, memoryPerCountIndex, "memoryPer(%)", titleStyle1)
outTable.write_string(0, deviceAppHashCountIndex, "deviceAppHash", titleStyle2)
outTable.write_string(0, appStartTimeCountIndex, "appStartTime", titleStyle1)

# 设置输出表 CountResult 列表字段title
outCountTable.write_string(0, 0, "Symbol", titleStyle1)
outCountTable.write_string(0, 1, "Count", titleStyle2)
outCountTable.write_string(0, 2, "Percentage(%)", titleStyle1)

# 全局符号缓存
symbolsCache = {}

# crashCount 表的输出信息来源
symbolDic = {}

# 输出表 CrashLog 中写入行号，每解析一行，写入行号加1
rowIndex = 0
crashOriginDataError = 0

# 支持多文件解析
for inputFile in crashFileList:

    try:
        crashFo = open(inputFile, "r+")
    except:
        print "Error: open file %s error. " % inputFile
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
    if not CJFKit.validateString(crashData):
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

    if not CJFKit.validateDictionary(crashDic):
        print "Error: file %s json decode failed." % inputFile
        crashOriginDataError += 1
        continue

    # 每解析一行，写入行号加1
    rowIndex += 1

    # 崩溃类型和原因:
    crashType = ""
    crashReason = ""
    crashCategory = ""

    # 写入文件名
    outTable.write_string(rowIndex, crashFileColumnIndex, str(inputFile), contentCenterStyle)

    try:
        crashCategory = crashDic["crash"]["error"]["type"]
    except:
        print "inputFile %s key error : crashCategory get error." % inputFile

    try:
        if CJFKit.validateString(crashCategory):
            if crashCategory == "nsexception":
                crashType = crashDic["crash"]["error"]["nsexception"]["name"]
            elif crashCategory == "mach":
                crashType = crashDic["crash"]["error"]["mach"]["exception_name"]
            elif crashCategory == "signal":
                crashType = crashDic["crash"]["error"]["signal"]["name"]
            else:
                crashType = crashDic["crash"]["error"]["signal"]["name"]
        else:
            crashType = crashDic["crash"]["error"]["signal"]["name"]
    except:
        print "inputFile %s key error : crashType get error." % inputFile
    outTable.write_string(rowIndex, typeColumnIndex, CJFKit.toValidateString(crashType), contentCenterStyle)

    try:
        crashReason = crashDic["crash"]["error"]["reason"]
    except:
        print "inputFile %s key error : crashReason get error -[reason]" % inputFile

    if not CJFKit.validateString(crashCategory):
        try:
            crashReason = crashDic["crash"]["diagnosis"]
        except:
            print "inputFile %s key error : crashReason get error -[diagnosis]." % inputFile
    outTable.write_string(rowIndex, reasonColumnIndex, CJFKit.toValidateString(crashReason), contentLeftStyle)

    # system内信息:
    crashJailbroken = False
    crashDeviceType = ""
    crashOsVersion = ""
    crashBackgroundTime = 0
    crashUseMemory = 0
    crashUnuseMemory = 0
    crashMemoryPer = 0.0
    crashDeviceAppHash = ""
    crashAppStartTime = ""
    crashArchiver = ""

    try:
        crashJailbroken = crashDic["system"]["jailbroken"]
    except:
        print "inputFile %s key error : crashJailbroken get error ." % inputFile
    outTable.write_boolean(rowIndex, jailbrokenColumnIndex, CJFKit.toValidateBool(crashJailbroken), contentCenterStyle)

    try:
        crashDeviceType = crashDic["system"]["machine"]
    except:
        print "inputFile %s key error : crashJailbroken get error ." % inputFile
    outTable.write_string(rowIndex, deviceTypeColumnIndex, CJFKit.toValidateString(crashDeviceType), contentCenterStyle)

    try:
        crashOsVersion = crashDic["system"]["system_version"]
    except:
        print "inputFile %s key error : crashOsVersion get error ." % inputFile
    outTable.write_string(rowIndex, osVersionColumnIndex, CJFKit.toValidateString(crashOsVersion), contentCenterStyle)

    # 此处取值字段 background_time_since_launch 可能需要调整
    try:
        crashBackgroundTime = crashDic["system"]["application_stats"]["background_time_since_launch"]
    except:
        print "inputFile %s key error : crashBackgroundTime get error ." % inputFile
    outTable.write_number(rowIndex, backgroundColumnIndex, CJFKit.toValidateNumber(crashBackgroundTime),
                          contentCenterStyle)

    try:
        crashUseMemory = crashDic["system"]["memory"]["usable"]
    except:
        print "inputFile %s key error : crashUseMemory get error ." % inputFile
    outTable.write_number(rowIndex, useMemoryColumnIndex, CJFKit.toValidateNumber(crashUseMemory), contentCenterStyle)

    try:
        crashUnuseMemory = crashDic["system"]["memory"]["free"]
    except:
        print "inputFile %s key error : crashUnuseMemory get error ." % inputFile
    outTable.write_number(rowIndex, unuseMemoryColumnIndex, CJFKit.toValidateNumber(crashUnuseMemory),
                          contentCenterStyle)

    if (CJFKit.validateInteger(crashUseMemory) and crashUseMemory > 0
        and CJFKit.validateInteger(crashUnuseMemory) and crashUnuseMemory >= 0):
        crashAllMemory = crashUseMemory + crashUnuseMemory
        crashMemoryPer = float(crashUseMemory) / crashAllMemory
        crashMemoryPer = crashMemoryPer * 100
        crashMemoryPer = float("%.2f" % crashMemoryPer)
    else:
        print "inputFile %s key error : crashMemoryPer deal error ." % inputFile
    outTable.write_number(rowIndex, memoryPerCountIndex, CJFKit.toValidateNumber(crashMemoryPer), contentCenterStyle)

    try:
        crashDeviceAppHash = crashDic["system"]["device_app_hash"]
    except:
        print "inputFile %s key error : crashDeviceAppHash get error ." % inputFile
    outTable.write_string(rowIndex, deviceAppHashCountIndex, CJFKit.toValidateString(crashDeviceAppHash),
                          contentCenterStyle)

    try:
        crashAppStartTime = crashDic["system"]["app_start_time"]
    except:
        print "inputFile %s key error : crashAppStartTime get error ." % inputFile
    outTable.write_string(rowIndex, appStartTimeCountIndex, CJFKit.toValidateString(crashAppStartTime),
                          contentCenterStyle)

    try:
        crashArchiver = crashDic["system"]["cpu_arch"]
    except:
        print "inputFile %s key error : crashArchiver get error ." % inputFile

    # 崩溃线程信息
    try:
        AllThreadData = crashDic["crash"]["threads"]
    except:
        print "inputFile %s key error : crash All thread get error ." % inputFile
        continue

    if not CJFKit.validateList(AllThreadData):
        print "inputFile %s key error : crash All thread type error ." % inputFile
        continue

    for crashThreadInfo in AllThreadData:
        threadCrashed = False
        try:
            threadCrashed = crashThreadInfo["crashed"]
        except:
            print "inputFile %s key error : threadCrashed get error ." % inputFile
        # 非crash线程目前暂不处理
        if not threadCrashed:
            continue

        crashSymbolList = []
        crashThreadIndex = 0
        try:
            crashThreadIndex = crashThreadInfo["index"]
        except:
            print "inputFile %s key error : crashThreadIndex get error ." % inputFile
        outTable.write_number(rowIndex, crashThreadIndexColumnIndex, CJFKit.toValidateNumber(crashThreadIndex),
                              contentCenterStyle)

        crashThreadRegisters = ""
        if CJFKit.validateDicElement(crashThreadInfo, "notable_addresses"):
            crashThreadRegisters = crashThreadRegisters + "notable_addresses"
        if CJFKit.validateDicElement(crashThreadInfo, "registers"):
            if CJFKit.validateString(crashThreadRegisters):
                crashThreadRegisters = crashThreadRegisters + " && " + "registers"
            else:
                crashThreadRegisters = crashThreadRegisters + "registers"
        if not CJFKit.validateString(crashThreadRegisters):
            crashThreadRegisters = "Nothings"
        outTable.write_string(rowIndex, crashRegisterInfoColumnIndex, crashThreadRegisters, contentCenterStyle)

        crashThreadStackInfo = []
        try:
            crashThreadStackInfo = crashThreadInfo["backtrace"]["contents"]
        except:
            print "inputFile %s key error : crashThreadStackInfo get error ." % inputFile

        if not CJFKit.validateList(crashThreadStackInfo):
            print "inputFile %s key error : crashThreadStackInfo type error ." % inputFile
            break

        for crashSingleSymbol in crashThreadStackInfo:
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

            if CJFKit.validateString(object_name) and object_name == target_app_run_name:
                pass
            else:
                continue

            # 符号化 instruction_addr
            crashInstructionParserKey = "%d_%d" % (object_addr, instruction_addr)
            crashInstructionParser = ""
            if symbolsCache.has_key(crashInstructionParserKey):
                crashInstructionParser = symbolsCache[crashInstructionParserKey]
                crashSymbolList.append(crashInstructionParser)
            else:
                crashInstructionParser = parseCrashByAddress(object_addr, instruction_addr, crashArchiver)
                if CJFKit.validateString(crashInstructionParser):
                    crashSymbolList.append(crashInstructionParser)
                    symbolsCache[crashInstructionParserKey] = crashInstructionParser

            # 符号化 symbol_addr, 需要 常量开关打开方可解析
            if target_need_symbol:
                crashSymbolParserKey = "%d_%d" % (object_addr, instruction_addr)
                crashSymbolParser = ""
                if symbolsCache.has_key(crashSymbolParserKey):
                    crashSymbolParser = symbolsCache[crashSymbolParserKey]
                    crashSymbolList.append(crashSymbolParser)
                else:
                    crashSymbolParser = parseCrashByAddress(object_addr, instruction_addr, crashArchiver)
                    if CJFKit.validateString(crashSymbolParser):
                        crashSymbolList.append(crashSymbolParser)
                        symbolsCache[crashSymbolParserKey] = crashSymbolParser

        if len(crashSymbolList) > 0 and CJFKit.validateString(crashSymbolList[0]):
            if symbolDic.has_key(crashSymbolList[0]):
                symbolDic[crashSymbolList[0]] += 1
            else:
                symbolDic[crashSymbolList[0]] = 1

        if len(crashSymbolList) > 0:
            outTable.write_string(rowIndex, crashSymbolColumnIndex, "".join(crashSymbolList), contentLeftStyle)
        break

# 越界保护
if rowIndex > 0:
    haveCount = 0
    index = 1
    for key in symbolDic.keys():
        haveCount = haveCount + symbolDic[key]
        per = float(symbolDic[key]) / rowIndex
        per = per * 100
        outCountTable.write_string(index, 0, key, contentCenterStyle)
        outCountTable.write_number(index, 1, symbolDic[key], contentCenterStyle)
        outCountTable.write_number(index, 2, float("%.4f" % (per)), contentCenterStyle)
        index = index + 1

    diff = rowIndex - haveCount
    per = float(diff) / rowIndex
    outCountTable.write_string(index, 0, "Nothing && Unknow", contentCenterStyle)
    outCountTable.write_number(index, 1, diff, contentCenterStyle)
    outCountTable.write_number(index, 2, float("%.4f" % (per)), contentCenterStyle)

    index = index + 1
    outCountTable.write_string(index, 0, "AllCount", contentCenterStyle)
    outCountTable.write_number(index, 1, rowIndex, contentCenterStyle)
    outCountTable.write_number(index, 2, 100.0000, contentCenterStyle)

# 保存excel
outFile.close()

# 打印汇总信息
print "\n\n\n#######################  Parser Report  #######################"
print "Parser crash success count : %d" % rowIndex
print "Parser crash data error count : %d" % crashOriginDataError
print "Crash parser output file: %s" % outFilePath
print "################################################################"
