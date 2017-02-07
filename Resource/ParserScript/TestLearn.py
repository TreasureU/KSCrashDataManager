# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #


"""
说明区:
	请使用命令: python JDiOSAllCrashConvertMutilProcess.py <iPad/iPhone> <fileDir> <localDir> <outPutDir>
	脚本将自动解析指定目录下的 *.json 文件,请将 KCrash上报的数据放置在里面.
	默认只解析 instruction_addr,如果需要同时解析 symbol_addr ,请将 target_need_symbol 常量置为 True .
	脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。
	如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True
"""

import glob
import os

import CJFKit

# --------------------   全局配置区  -----------------------




# --------------------   全局函数去  -----------------------

def validateString(obj):
    # 需要兼顾 basestring \ str \ unicode 三种字符串类情况
    if isinstance(obj, basestring) and len(obj) > 0:
        return True
    else:
        return False


def validateList(obj):
    if isinstance(obj, list) and len(obj) > 0:
        return True
    else:
        return False


def recursionGetAllDirInSpecialDir(specifyDirName, needPathName = False, notNeedHideElement = True):
    if not validateString(specifyDirName):
        return None
    if not os.path.isdir(specifyDirName):
        return None
    resultList = []
    subLeafList = os.listdir(specifyDirName)
    for element in subLeafList:
        if os.path.isdir(specifyDirName + "/" + element):
            if element.find(".") == 0 and notNeedHideElement:
                continue
            if needPathName:
                resultList.append(specifyDirName + "/" + element)
            else:
                resultList.append(element)
            subList = recursionGetAllDirInSpecialDir(specifyDirName + "/" + element, needPathName, notNeedHideElement)
            resultList.extend(subList)
    return resultList


def recursionGetSpecialFilesInSpecialDir(specifyDirName, formatStr, needPathName = False, notNeedHideElement = True):
    if not validateString(specifyDirName):
        return None
    if not os.path.isdir(specifyDirName):
        return None
    subDirResultList = recursionGetAllDirInSpecialDir(specifyDirName, True)
    dirResultList = [specifyDirName]
    resultList = []
    if validateList(subDirResultList):
        dirResultList.extend(subDirResultList)
    for element in dirResultList:
        sourceSubList = glob.glob(element + "/" + formatStr)
        subList = []
        if validateList(sourceSubList):
            for filePath in sourceSubList:
                if not os.path.isfile(filePath):
                    continue
                if notNeedHideElement and os.path.basename(filePath)[0] == ".":
                    continue
                if not needPathName:
                    subList.append(os.path.basename(filePath))
                else:
                    subList.append(filePath)
        resultList.extend(subList)
    return resultList


def isVerifyExt(ext):
    global global_file_ext_list


# 返回主用户目录
def getHomeDirPath():
    ret = os.environ["HOME"]
    if validateString(ret):
        return ret
    ret = os.path.expandvars("$HOME")
    if validateString(ret):
        return ret
    ret = os.path.expanduser("~")
    if validateString(ret):
        return ret
    return ""

# 返回转化后的目录
def getAbsolutePath(filePath):
    if not validateString(filePath):
        return None
    if filePath[0:2] == "~/":
        return getHomeDirPath() + filePath[1:]
    else:
        return filePath


# --------------------   正式代码区   -----------------------

print os.environ["HOME"]
print os.path.expandvars("$HOME")
print os.path.expanduser("~")

print type(os.environ["HOME"])
print type(os.path.expandvars("$HOME"))
print type(os.path.expanduser("~"))

search_path = "~/Library/Developer/Xcode/iOS DeviceSupport"
if search_path[0:2] == "~/":
    search_path = os.environ["HOME"] + search_path[1:]
print search_path

lists = CJFKit.recursionGetAllDirInSpecialDir(search_path)
print lists

