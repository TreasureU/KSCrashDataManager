# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

import datetime
import time

import baseEx


# 将UTC时间转化为东-8时间
def UTCTimeStrToLocalTimeStr(utcTimerStr, utcFormatStr = "%Y-%m-%dT%H:%M:%SZ", localFormatStr = "%Y-%m-%d %H:%M:%S"):
    if not baseEx.validateString(utcTimerStr) or not baseEx.validateString(utcFormatStr) or not baseEx.validateString(
            localFormatStr):
        return None
    try:
        utcDate = datetime.datetime.strptime(utcTimerStr, utcFormatStr)
    except:
        return None

    localDate = utcDate + datetime.timedelta(hours = 8)
    try:
        localStr = localDate.strftime(localFormatStr)
    except:
        return None
    return localStr


# str -> date obj
def safeGetDateObjFormStr(timeStr, formatStr = "%Y-%m-%d %H:%M:%S"):
    if not baseEx.validateString(timeStr) or not baseEx.validateString(formatStr):
        return None
    try:
        dateObj = datetime.datetime.strptime(timeStr, formatStr)
    except:
        return None
    return dateObj


# 获得相对于配置固定时间点的时间间隔
def getMKTimeInterval(sourceDate):
    if not isinstance(sourceDate, datetime.datetime):
        return None
    timeStruct = sourceDate.timetuple()
    return time.mktime(timeStruct)


# 获取两个时间对象之间的时间间隔
def getTimeInterval(sourceDate, targetDate):
    sourceTime = getMKTimeInterval(sourceDate)
    targetTime = getMKTimeInterval(targetDate)
    if isinstance(sourceTime, float) and isinstance(targetTime, float):
        timeInterval = sourceTime - targetTime
        return timeInterval
    return None


def getTimeIntervalByStr(sourceDataStr, targetDateStr, formatStr = "%Y-%m-%d %H:%M:%S"):
    sourceDate = safeGetDateObjFormStr(sourceDataStr, formatStr)
    targetDate = safeGetDateObjFormStr(targetDateStr, formatStr)
    if sourceDate and targetDate:
        return getTimeInterval(sourceDate, targetDate)
    else:
        return None
