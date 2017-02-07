# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
	请使用命令: python JDiOSOOMClassify.py <iPad/iPhone> <fileDir> <BG/AT/IA/FG/None>
	脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.
	脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
	如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import os, glob, sys, json, re, urllib
import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False
target_oom_dir = None
target_oom_source_dir = None
target_device_type = None

target_iPad_url_nav = ["JDWebViewController"]
target_iPhone_url_nav = ["WareInfoBViewController", "JDWebViewController"]


# ----------------------------------  函数定义区 --------------------------------------- #

def safeSymbolLinkCrashFile(fileName, dstName, dirName):
    # global target_input_filedir
    fileName = dirName + "/" + fileName
    CJFKit.safeSymbolLink(fileName, dstName)


# ----------------------------------  正式代码区域 -------------------------------------- #

if not target_debug_flag:
    if len(sys.argv) >= 4:
        target_device_type = sys.argv[1]
        target_input_filedir = sys.argv[2]
        OOMDir = sys.argv[3]

        if CJFKit.validateString(target_device_type) and (
                        target_device_type == "iPhone" or target_device_type == "iPad"):
            pass
        else:
            print "Error: Device type is error. Please use : iPhone / iPad"
            sys.exit(-1)

        if OOMDir == "AT":
            target_oom_dir = target_input_filedir + "/oom/AT_classify"
            target_oom_source_dir = target_input_filedir + "/oom/AT"
        elif OOMDir == "BG":
            target_oom_dir = target_input_filedir + "/oom/BG_classify"
            target_oom_source_dir = target_input_filedir + "/oom/BG"
        elif OOMDir == "FG":
            target_oom_dir = target_input_filedir + "/oom/FG_classify"
            target_oom_source_dir = target_input_filedir + "/oom/FG"
        elif OOMDir == "IA":
            target_oom_dir = target_input_filedir + "/oom/IA_classify"
            target_oom_source_dir = target_input_filedir + "/oom/IA"
        elif OOMDir == "None":
            target_oom_dir = target_input_filedir + "/oom/None_classify"
            target_oom_source_dir = target_input_filedir + "/oom/None"
        else:
            print "Error: OOMDir is error. Please use : AT/BG/FG/IA/None"
            sys.exit(-1)
    else:
        print "Error: need origin fileDir Param. Please use : python JDiPadCrashParser.py <fileDir>"
        sys.exit(-1)
else:
    target_device_type = "iPhone"
    OOMDir = "AT"
    target_input_filedir = "../5.2.1_PPcrash_0905"
    target_oom_dir = target_input_filedir + "/oom/AT_classify"
    target_oom_source_dir = target_input_filedir + "/oom/AT"

# 新建OOM分类文件夹
CJFKit.safeClearDir(target_oom_dir)
CJFKit.safeRemovePath(target_input_filedir + "/oom/" + OOMDir + "_NavResult")
CJFKit.safeRemovePath(target_input_filedir + "/oom/" + OOMDir + "_UrlResult")

file_error_count = 0
file_error_list = []
file_controlller_dic = {}
file_url_dic = {}

needClassifyFileList = glob.glob(target_oom_source_dir + "/*.json")
allFileCount = len(needClassifyFileList)
if allFileCount <= 0:
    print "Warning: %s is no *.json file" % target_oom_source_dir
    sys.exit(-1)

for needClassifyFileName in needClassifyFileList:
    needClassifyFileStr = CJFKit.safeGetFileContentStr(needClassifyFileName, True)
    if not CJFKit.validateString(needClassifyFileStr):
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

    last_nav_history = CJFKit.safeGetElement(needClassifyFileJson, ["nav", -1, "c"])
    if not CJFKit.validateString(last_nav_history):
        last_nav_history = "None"
    if not os.path.isdir(target_oom_dir + "/" + last_nav_history):
        os.mkdir(target_oom_dir + "/" + last_nav_history)
    if file_controlller_dic.has_key(last_nav_history):
        file_controlller_dic[last_nav_history]["count"] += 1
    else:
        tmpdic = {}
        tmpdic["count"] = 1
        tmpdic["name"] = last_nav_history
        file_controlller_dic[last_nav_history] = tmpdic

    # 判断是否需要进入url分类
    needUrlClassify = False
    if target_device_type == "iPhone":
        for navName in target_iPhone_url_nav:
            if last_nav_history == navName:
                needUrlClassify = True
                break
    elif target_device_type == "iPad":
        for navName in target_iPad_url_nav:
            if last_nav_history == navName:
                needUrlClassify = True
                break

    if needUrlClassify:
        last_url_history = CJFKit.safeGetElement(needClassifyFileJson, ["url", -1, "u"])
        if CJFKit.validateString(last_url_history):
            pattern = re.compile(r'&to=.*')
            result = pattern.search(last_url_history)
            if result and CJFKit.validateString(result.group()):
                last_url_history = result.group()
                loc = last_url_history.find("&action=")
                if loc >= 0:
                    last_url_history = last_url_history[0:loc]
                last_url_history = last_url_history[4:]
        if not CJFKit.validateString(last_url_history):
            last_url_history = "None"
        else:
            last_url_history = urllib.unquote(last_url_history)

        if file_url_dic.has_key(last_url_history):
            file_url_dic[last_url_history]["count"] += 1
        else:
            tmpdic = {}
            tmpdic["name"] = last_url_history
            tmpdic["count"] = 1
            tmpdic["dirName"] = str(len(file_url_dic))
            file_url_dic[last_url_history] = tmpdic

        # 归类到不同的文件夹中,但是统计在同一项中
        if not os.path.isdir(target_oom_dir + "/" + last_nav_history + "/" + file_url_dic[last_url_history]["dirName"]):
            os.mkdir(target_oom_dir + "/" + last_nav_history + "/" + file_url_dic[last_url_history]["dirName"])

        outputFileName = target_oom_dir + "/" + last_nav_history + "/" + file_url_dic[last_url_history][
            "dirName"] + "/" + os.path.basename(
                needClassifyFileName)
        safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName, "../../../" + OOMDir)
    else:
        outputFileName = target_oom_dir + "/" + last_nav_history + "/" + os.path.basename(
                needClassifyFileName)
        safeSymbolLinkCrashFile(os.path.basename(needClassifyFileName), outputFileName, "../../" + OOMDir)

oom_classify_reports = file_controlller_dic.values()
for tmpdic in oom_classify_reports:
    tmpdic["precentage"] = tmpdic["count"] * 100.0 / allFileCount

url_classify_reports = file_url_dic.values()
for tmpdic in url_classify_reports:
    tmpdic["precentage"] = tmpdic["count"] * 100.0 / allFileCount

oom_classify_reports.sort(key = lambda x:x["count"], reverse = True)
CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/" + OOMDir + "_NavResult", oom_classify_reports)

url_classify_reports.sort(key = lambda x:x["count"], reverse = True)
CJFKit.safeWriteFileContentJSON(target_input_filedir + "/oom/" + OOMDir + "_UrlResult", url_classify_reports)

print "OOM Classify done"
