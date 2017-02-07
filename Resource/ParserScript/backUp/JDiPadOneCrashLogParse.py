# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
	需要把 .dSYM文件或者是.app 文件放置在指定目录下
	指令类似于 python xxipadOneCrashLogParse.py <iPad/iPhone>  <arch> <baseAddr> <symbolAddr>
	arch 必须是以下取值: armv7 \ armv7s \ arm64 \ armv7f
	baseAddr 和 symbolAddr 必须是16进制数
	如果希望直接使用指令,可以参考如下:
	atos -arch armv7  -o ../SourceSymbol/xxipad/xxipad -l 962560 2666928
"""

import sys, os, CJFKit


# ----------------------------------  常量定义区域 -------------------------------------- #

# 全局调试宏,暂时未使用到
target_debug_flag = False

# dSYM解析效果更好,优先用于解析
# symbol file path
global_symbol_ipad_file = "../SourceSymbol/xxipad/xxipad"
global_symbol_iphone_file = "../SourceSymbol/xxxiPhone/xxxiPhone"
target_symbol_file = None

# ----------------------------------  正式代码区域 -------------------------------------- #

if len(sys.argv) != 5:
    print "Please Use : python xxipadOneCrashLogParse.py <iPad/iPhone> <arch> <baseAddr> <symbolAddr> , addr is decimal system"
    sys.exit(-1)

try:
    appName = sys.argv[1]
    arch = sys.argv[2]
    baseAddress = int(sys.argv[3])
    symbolAddress = int(sys.argv[4])
except:
    print "Error: param convert error"
    sys.exit(-1)

if CJFKit.validateString(appName) and (appName == "iPad" or appName == "iPhone"):
    if appName == "iPad":
        target_symbol_file = global_symbol_ipad_file
    else:
        target_symbol_file = global_symbol_iphone_file
else:
    print "Error: AppName is not iPad or iPhone.\n"
    sys.exit(-1)

# 校验有效文件
if not os.path.isfile(target_symbol_file):
    print "Error: need origin file in the dir , like %s" % (target_symbol_file)
    sys.exit(-1)

if not CJFKit.validateInteger(baseAddress):
    print "Error: baseAddress is not a decimal system Integer\n"
    sys.exit(-1)
if not CJFKit.validateInteger(symbolAddress):
    print "Error: symbolAddress is not a decimal system Integer\n"
    sys.exit(-1)
if baseAddress <= 0:
    print "Error: baseAddress need greate than 0\n"
    sys.exit(-1)
if symbolAddress <= 0:
    print "Error: symbolAddress need greate than 0\n"
    sys.exit(-1)

# 格式一共分为 arm64\armv7\armv7s\armv7f,架构iPad与iPhone一致
if CJFKit.validateString(arch) and arch == "arm64":
    pass
else:
    arch = "armv7"

cmd = ("atos -arch " + arch + " -o %s -l " % target_symbol_file
       + "0x%x" % baseAddress + " " + "0x%x" % symbolAddress)
# print cmd
outStr = os.popen(cmd).read()
if isinstance(outStr, str) and len(outStr) > 0:
    print outStr
    sys.exit(0)
else:
    print "Parse failed\n"
    sys.exit(-1)
