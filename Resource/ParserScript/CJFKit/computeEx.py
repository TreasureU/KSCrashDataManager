# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

import numpy
import baseEx


# 计算标准平均值
def averageNumberList(seq):
    if baseEx.validateList(seq):
        return float(sum(seq)) / len(seq)
    else:
        return 0.0


# 计算标准方差值
def varNumberList(seq):
    if baseEx.validateList(seq):
        numList = numpy.array(seq)
        return numpy.var(numList)
    else:
        return 0.0
