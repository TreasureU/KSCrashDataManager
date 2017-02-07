# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

import baseEx
import computeEx


class systemCrashModel:
    def __init__(self, name, fileDirName):
        self.fileDirName = fileDirName
        self.count = 0
        self.percentage = 0.0
        self.canFix = None
        self.description = name
        self.keyWord = None
        self.keyWords = None
        self.keyWordList = None
        self.param = None
        self.controllers = None
        self._checkParam()

    def __str__(self):
        return "[fileDirName = %s, count = %d , percentage = %f]" % (self.fileDirName, self.count, self.percentage)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def dictToSystemCrashModel(cls, dataDict):
        if not baseEx.validateDictionary(dataDict):
            return None
        fileDirName = baseEx.safeGetDicElement(dataDict, "fileDirName")
        if baseEx.validateString(fileDirName):
            ret = systemCrashModel("", fileDirName)
            ret.description = baseEx.safeGetDicElement(dataDict, "description")
            ret.canFix = baseEx.safeGetDicElement(dataDict, "canFix")
            ret.keyWords = baseEx.safeGetDicElement(dataDict, "keyWords")
            ret.keyWord = baseEx.safeGetDicElement(dataDict, "keyWord")
            ret.keyWordList = baseEx.safeGetDicElement(dataDict, "keyWordList")
            ret.param = baseEx.safeGetDicElement(dataDict, "param")
            ret._checkParam()
            return ret
        else:
            return None

    def convertToDict(self):
        retDict = {
            "fileDirName":self.fileDirName,
            "count":self.count,
            "percentage":self.percentage,
            "canFix":self.canFix,
            "description":self.description
        }
        if self.keyWords:
            retDict["condition"] = self.keyWords
        elif self.keyWord:
            retDict["condition"] = self.keyWord
        elif self.keyWordList:
            retDict["condition"] = self.keyWordList
        else:
            retDict["condition"] = None
        return retDict

    def convertToSymbolDict(self):
        retDict = {
            "fileDirName":self.fileDirName,
            "count":self.count,
            "percentage":self.percentage,
            "canFix":True,
            "description":self.description
        }
        return retDict

    def _checkParam(self):
        # if self.param and CJFKit.safeGetDicElement(self.param, classifyByController):
        self.controllers = {}
        self.OSversions = {}
        self.deviceType = {}
        # 内存告警数据存储点
        self.mwTimeList = []
        self.atTimeList = []
        self.bgTimeList = []

    def addController(self, controllerName):
        # if not isinstance(self.controllers, dict):
        #     return
        if self.controllers.has_key(controllerName):
            self.controllers[controllerName] += 1
        else:
            self.controllers[controllerName] = 1

    def addOSversion(self, osVersion):
        # if not isinstance(self.OSversions, dict):
        #     return
        if self.OSversions.has_key(osVersion):
            self.OSversions[osVersion] += 1
        else:
            self.OSversions[osVersion] = 1

    def addDeviceType(self, deviceType):
        # if not isinstance(self.deviceType, dict):
        #     return
        if self.deviceType.has_key(deviceType):
            self.deviceType[deviceType] += 1
        else:
            self.deviceType[deviceType] = 1

    def addMWTimerInterval(self, time):
        if baseEx.validateNumber(time) and time >= 0:
            self.mwTimeList.append(time)

    def addATTimerInterval(self, time):
        if baseEx.validateNumber(time) and time >= 0:
            self.atTimeList.append(time)

    def addBGTimerInterval(self, time):
        if baseEx.validateNumber(time) and time >= 0:
            self.bgTimeList.append(time)

    @classmethod
    def getSortListFormDict(cls, countDic):
        if not baseEx.validateDictionary(countDic):
            return None
        retList = []
        allCount = 0
        for key in countDic.keys():
            allCount += countDic[key]
        for key in countDic.keys():
            dataDic = {}
            dataDic["name"] = key
            dataDic["count"] = countDic[key]
            dataDic["percentage"] = countDic[key] * 100.0 / allCount
            retList.append(dataDic)
        retList.sort(key = lambda x:x["count"], reverse = True)
        return retList

    def getCrashAssitInfo(self):
        assitInfoDict = {}
        assitInfoDict["controllerSort"] = systemCrashModel.getSortListFormDict(self.controllers)
        assitInfoDict["OSversionsSort"] = systemCrashModel.getSortListFormDict(self.OSversions)
        assitInfoDict["deviceTypeSort"] = systemCrashModel.getSortListFormDict(self.deviceType)

        active_timeCount = computeEx.averageNumberList(self.atTimeList)
        background_timeCount = computeEx.averageNumberList(self.bgTimeList)
        mw_timeCount = computeEx.averageNumberList(self.mwTimeList)
        mw_varValue = computeEx.varNumberList(self.mwTimeList)

        assitInfoDict["timeCostCount"] = {
            "global_active_timeCount":active_timeCount,
            "global_launch_timeCount":active_timeCount + background_timeCount,
            "global_background_timeCount":background_timeCount,
            "global_mw_timeCount":mw_timeCount,
            "global_mw_timeVariance":mw_varValue,
            "global_mw_timeNumber":len(self.mwTimeList)
        }

        return assitInfoDict
