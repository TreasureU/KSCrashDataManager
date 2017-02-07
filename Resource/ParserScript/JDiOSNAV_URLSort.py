# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    快速对文件夹下的NAV与URL进行归类统计
    请使用命令: python JDiOSNAV_URLSort.py <iPad/iPhone> <sourceDir> <localDir> <OutPutName>
    示例: python JDiOSNAV_URLSort.py ../530_appstore_11AM sortOut/BG sortOut/BG_RESULT
    后两个路径是以第一个路径为当前目录的相对路径
    脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.
    脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
    如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import copy
import json
import re
import sys
import urllib

import CJFKit


# ----------------------------------  全局变量定义区域 -------------------------------------- #

# 全局调试宏
target_debug_flag = False
target_allVC_needURL = False

target_device_type = None
target_source_dir = None
target_sort_source_dir = None
target_sort_outputDirName = None
target_isOOM = False

# target_nav_count_url_list = None
# target_url_prefix_list = None

global_iPad_name = "iPad"
global_iPhone_name = "iPhone"

global_iPad_setting_name = "./setting/NavAndUrlSortiPad.json"
global_iPhone_setting_name = "./setting/NavAndUrlSortiPhone.json"

global_url_osVersion_dic = {}
global_url_deviceType_dic = {}


# ----------------------------------  函数定义区 --------------------------------------- #

def addValueCount(countDic, key):
    if countDic.has_key(key):
        countDic[key] += 1
    else:
        countDic[key] = 1


# 将值字典转化为
def convertDictoList(countDic):
    if not CJFKit.validateDictionary(countDic):
        return None

    retList = []

    allCount = 0
    for key in countDic.keys():
        allCount += countDic[key]

    for key in countDic.keys():
        dataDic = {"name":key,
                   "count":countDic[key],
                   "percentage":countDic[key] * 100.0 / allCount}
        retList.append(dataDic)

    retList.sort(key = lambda x:x["count"], reverse = True)
    return retList


# ----------------------------------  正式代码区 --------------------------------------- #

if not target_debug_flag:
    if len(sys.argv) >= 5:
        target_device_type = sys.argv[1]
        target_source_dir = sys.argv[2]
        target_sort_source_dir = target_source_dir + "/" + sys.argv[3]
        target_sort_outputDirName = target_source_dir + "/" + sys.argv[4]

        if CJFKit.validateString(target_device_type) and (
                target_device_type == global_iPhone_name or target_device_type == global_iPad_name):
            pass
        else:
            print "Error: Device type is error. Please use : iPhone / iPad"
            sys.exit(-1)
    else:
        print "Error: need origin fileDir Param. Please use : python JDiOSNAV_URLSort.py <iPad/iPhone> <sourceDir> <localDir> <OutPutName>"
        sys.exit(-1)
else:
    target_device_type = "iPhone"
    target_source_dir = "../crash0110_15_16_560"
    target_sort_source_dir = "../crash0110_15_16_560/sortOut/crash_system/33"
    target_sort_outputDirName = "../crash0110_15_16_560/crash_system/33_Result"

# 初始化设置文件
if target_device_type == global_iPhone_name:
    setting_file_content = CJFKit.safeGetFileContentJSON(global_iPhone_setting_name)
else:
    setting_file_content = CJFKit.safeGetFileContentJSON(global_iPad_setting_name)
target_nav_count_url_list = CJFKit.safeGetDicElement(setting_file_content, "nav")
target_url_prefix_list = CJFKit.safeGetDicElement(setting_file_content, "url_pre")

if target_nav_count_url_list is None:
    target_nav_count_url_list = []
if target_url_prefix_list is None:
    target_url_prefix_list = []

if target_sort_source_dir.find("/oom/") >= 0:
    target_isOOM = True

CJFKit.safeClearDir(target_sort_outputDirName)

file_error_count = 0
file_error_list = []
file_controlller_dic = {}
file_url_dic = {}

needClassifyFileList = CJFKit.recursionGetSpecialFilesInSpecialDir(target_sort_source_dir, "*.json", True, True)
if not CJFKit.validateList(needClassifyFileList):
    print "Error:%s is no *.json file" % target_sort_source_dir
    sys.exit(0)

allFileCount = len(needClassifyFileList)
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

    if target_isOOM:
        last_nav_history = CJFKit.safeGetElement(needClassifyFileJson, ["nav", -1, "c"])
    else:
        last_nav_history = CJFKit.safeGetElement(needClassifyFileJson, [-1, "user", "nav_history", -1, "c"])
    if not CJFKit.validateString(last_nav_history):
        last_nav_history = "None"
    if file_controlller_dic.has_key(last_nav_history):
        file_controlller_dic[last_nav_history]["count"] += 1
    else:
        tmpdic = {"count":1,
                  "name":last_nav_history}
        file_controlller_dic[last_nav_history] = tmpdic

    # 判断是否需要进入url分类
    needUrlClassify = target_allVC_needURL
    if target_device_type == "iPhone":
        # noinspection PyTypeChecker
        for navName in target_nav_count_url_list:
            if last_nav_history == navName:
                needUrlClassify = True
                break
    elif target_device_type == "iPad":
        # noinspection PyTypeChecker
        for navName in target_nav_count_url_list:
            if last_nav_history == navName:
                needUrlClassify = True
                break

    if needUrlClassify:
        if target_isOOM:
            last_url_history = CJFKit.safeGetElement(needClassifyFileJson, ["url", -1, "u"])
            os_version = CJFKit.safeGetElement(needClassifyFileJson, ["essential_sys", "system_version"])
            device_type = CJFKit.safeGetElement(needClassifyFileJson, ["essential_sys", "machine"])
        else:
            last_url_history = CJFKit.safeGetElement(needClassifyFileJson, [-1, "user", "url_history", -1, "u"])
            os_version = CJFKit.safeGetElement(needClassifyFileJson, [0,"system", "system_version"])
            device_type = CJFKit.safeGetElement(needClassifyFileJson, [0,"system", "machine"])
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
        # noinspection PyTypeChecker
        for need_cut_url in target_url_prefix_list:
            if need_cut_url in last_url_history:
                last_url_history = need_cut_url
                break

        if not CJFKit.validateString(os_version):
            os_version = "None"
        if not CJFKit.validateString(device_type):
            device_type = "None"

        if file_url_dic.has_key(last_url_history):
            file_url_dic[last_url_history]["count"] += 1
        else:
            tmpdic = {"name":last_url_history,
                      "count":1,
                      "osVersionDic":{},
                      "deviceTypeDic":{}}
            file_url_dic[last_url_history] = tmpdic

        addValueCount(file_url_dic[last_url_history]["osVersionDic"], os_version)
        addValueCount(file_url_dic[last_url_history]["deviceTypeDic"], device_type)

nav_classify_reports = file_controlller_dic.values()
for tmpdic in nav_classify_reports:
    tmpdic["precentage"] = tmpdic["count"] * 100.0 / allFileCount

url_classify_reports = file_url_dic.values()
url_osVersion_deviceType_reports = copy.deepcopy(url_classify_reports)

for tmpdic in url_classify_reports:
    tmpdic["precentage"] = tmpdic["count"] * 100.0 / allFileCount
    del tmpdic["osVersionDic"]
    del tmpdic["deviceTypeDic"]

# 应H5要求给出设备号和osverison
url_osVersion_deviceType_list = []
for tmpdic in url_osVersion_deviceType_reports:
    tmpdic["precentage"] = tmpdic["count"] * 100.0 / allFileCount
    tmpdic["osVersionSort"] = convertDictoList(tmpdic["osVersionDic"])
    tmpdic["deviceTypeSort"] = convertDictoList(tmpdic["deviceTypeDic"])
    del tmpdic["osVersionDic"]
    del tmpdic["deviceTypeDic"]
    url_osVersion_deviceType_list.append(tmpdic)

nav_classify_reports.sort(key = lambda x:x["count"], reverse = True)
CJFKit.safeWriteFileContentJSON(target_sort_outputDirName + "/URLSort_NavResult", nav_classify_reports)

url_classify_reports.sort(key = lambda x:x["count"], reverse = True)
CJFKit.safeWriteFileContentJSON(target_sort_outputDirName + "/URLSort__UrlResult", url_classify_reports)

url_osVersion_deviceType_list.sort(key = lambda x:x["count"], reverse = True)
CJFKit.safeWriteFileContentJSON(target_sort_outputDirName + "/OSVersion_DeviceType_Result",
                                url_osVersion_deviceType_list)

print "%s Classify done" % target_sort_source_dir
