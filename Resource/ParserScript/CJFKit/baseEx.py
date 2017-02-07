# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

from collections import Iterable


# 容器数据获取校验函数
def validateDicElement(obj, key):
    if isinstance(obj, dict) and obj.has_key(key):
        return True
    else:
        return False


# 判断是否可以从列表安全的获取数据,需要考虑index为正负数两种情况
def validateListElement(obj, index):
    if isinstance(obj, list):
        if 0 <= index < len(obj):
            return True
        elif index < 0 and len(obj) >= abs(index):
            return True
    return False


# 容器数据安全获取函数
def safeGetDicElement(obj, key):
    # type: (object, object) -> object
    if validateDicElement(obj, key):
        return obj[key]
    else:
        return None


def safeGetArrayIndex(obj, index):
    if validateListElement(obj, index):
        return obj[index]
    else:
        return None


# 传入key Iterable,可以接受中间元素是dic或者list
def safeGetElement(obj, keyList):
    if (validateDictionary(obj) or validateList(obj)) and isinstance(keyList, Iterable):
        value = obj
        for key in keyList:
            if validateDicElement(value, key) or validateListElement(value, key):
                value = value[key]
            else:
                return None
        return value
    return None


# 合法类型转换函数
def toValidateString(obj):
    if isinstance(obj, basestring):
        return obj
    else:
        return ""


def toValidateNumber(obj):
    if validateNumber(obj):
        return obj
    else:
        return 0


# 默认返回False
def toValidateBool(obj):
    if isinstance(obj, bool) and obj:
        return True
    else:
        return False


# 数据类型校验函数
def validateSet(obj):
    if isinstance(obj, set) and len(set) > 0:
        return True
    else:
        return False


def validateString(obj):
    # 需要兼顾 basestring \ str \ unicode 三种字符串类情况
    if isinstance(obj, basestring) and len(obj) > 0:
        return True
    else:
        return False


def validateDictionary(obj):
    if isinstance(obj, dict) and len(obj) > 0:
        return True
    else:
        return False


def validateList(obj):
    if isinstance(obj, list) and len(obj) > 0:
        return True
    else:
        return False


def validateNumber(obj):
    if isinstance(obj, int):
        return True
    elif isinstance(obj, long):
        return True
    elif isinstance(obj, float):
        return True
    else:
        return False


def validateInteger(obj):
    if isinstance(obj, int):
        return True
    elif isinstance(obj, long):
        return True
    else:
        return False


# set操作中,|表示合集,&表示交集,-表示A相对于B的补集,^表示双方的差集
# list合集操作
def listGetAaddBSet(a, b):
    if validateList(a) and not validateList(b):
        return set(a)
    elif validateList(b) and not validateList(a):
        return set(b)
    elif validateList(a) and validateList(b):
        return set(a) | set(b)
    else:
        return set()


# list补集操作
def listGetAsubBSet(a, b):
    if validateList(a) and not validateList(b):
        return set(a)
    elif validateList(b) and not validateList(a):
        return set()
    elif validateList(a) and validateList(b):
        return set(a) - set(b)
    else:
        return set()


# list差集操作
def listGetAdefBSet(a, b):
    if validateList(a) and not validateList(b):
        return set(a)
    elif validateList(b) and not validateList(a):
        return set(b)
    elif validateList(a) and validateList(b):
        return set(a) ^ set(b)
    else:
        return set()


# list交集操作
def listGetAmixBSet(a, b):
    if validateList(a) and not validateList(b):
        return set()
    elif validateList(b) and not validateList(a):
        return set()
    elif validateList(a) and validateList(b):
        return set(a) & set(b)
    else:
        return set()
