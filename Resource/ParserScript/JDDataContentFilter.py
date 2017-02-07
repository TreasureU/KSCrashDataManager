# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #


"""
说明区:
    快速统计指定文件夹下的含有特定文件内容的文件有多少
"""

import os
import sys

import CJFKit


target_debug_flag = False
target_input_dir = None

if not target_debug_flag:
    if len(sys.argv) >= 2:
        target_input_dir = sys.argv[1]
    else:
        print "Error: need origin fileDir Param. Please use : python JDiPadCrashParser.py <iPad/iPhone> <fileDir>"
        sys.exit(-1)
else:
    target_input_dir = "../iPhone_550_PP3"

target_input_filedir = target_input_dir + "/source"
CJFKit.safeCreateDir(target_input_dir + "/emptyProcess")
CJFKit.safeCreateDir(target_input_dir + "/haveContentProcess")

allCount = 0
emptyProcessCount = 0
haveContentProcessCount = 0

filelist = CJFKit.getAllFilesInSpecialDir(target_input_filedir, True)

if not CJFKit.validateList(filelist):
    print "not have source"
else:
    allCount = len(filelist)
    for filePath in filelist:
        # fileContent = CJFKit.safeGetFileContentStr(filePath)
        # if fileContent and ("Gray_550_PP3" in fileContent):
        # 	allCount += 1
        # 	print filePath
        allCount += 1
        fileContent = CJFKit.safeGetFileContentJSON(filePath)
        process = CJFKit.safeGetDicElement(fileContent, "process")
        if CJFKit.validateDictionary(process):
            haveContentProcessCount += 1
            CJFKit.safeWriteFileContentJSON(
                    target_input_dir + "/haveContentProcess/" + os.path.basename(filePath), fileContent)
        elif isinstance(process, dict):
            emptyProcessCount += 1
            CJFKit.safeWriteFileContentJSON(
                    target_input_dir + "/emptyProcess/" + os.path.basename(filePath), fileContent)
    print "all count :%d , emptyProcessCount : %d , haveContentProcessCount : %d .\n" % (
        allCount, emptyProcessCount, haveContentProcessCount)
