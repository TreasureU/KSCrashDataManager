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
import logging
import os
import sys
import traceback
from multiprocessing import Manager

import CJFKit


# 多线程相关变量
manager = Manager()
vagueMappingDict = manager.dict()

# --------------------   全局配置区  -----------------------

global_dir_name = "../iPad_390_1125"
global_file_ext_list = ["PNG", "JPG", "JPEG"]
global_debug_switch = False


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


def testtest():
    testest1()


def testest1():
    global aaaa
    print aaaa


def div(a, b):
    try:
        print(a / b)
    except (ZeroDivisionError, TypeError) as e:
        print("Error: b should not be 0 !!")
        print type(e)
    except Exception as e:
        print("Unexpected Error: {}".format(e))
        # print type(e)
    else:
        print('Run into else only when everything goes well')
    finally:
        print('Always run into finally block.')


# --------------------   正式代码区   -----------------------

str1 = CJFKit.safeGetFileContentStr("../iPad_390_1125/source/0d775177a5a1709008278cda60d4737ba2068a4d_OPTRHEGM.json")
str2 = CJFKit.safeGetFileContentStr("../iPad_390_1125/source/0d775177a5a1709008278cda60d4737ba2068a4d_OPTRHEGM.json")
str3 = CJFKit.safeGetFileContentStr("../iPad_390_1125/source/1c14c1696282277c7bbcb7b5ad5e62e6cc062439_YHIEQNFK.json")
if str1 == str2:
    print "str1 == str2:equal"
else:
    print "str1 == str2:not equal"

if str1 == str3:
    print "str1 == str3:equal"
else:
    print "str1 == str3:not equal"