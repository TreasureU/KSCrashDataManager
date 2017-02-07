# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

# 建议使用这种方式,默认是非阻塞执行
import subprocess
import baseEx


# warnning:注意调用的子进程输出信息不能过多,否则subprocess.PIPE可能无法承载,导致程序卡机.
# 此时需要我们另外设置一个文件对象

# 阻塞调用,返回输出结果
def sync_excuteCMD_output(cmdStr, isNeedPrint = False):
    if not baseEx.validateString(cmdStr):
        return ""
    try:
        obj = subprocess.Popen(cmdStr, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        obj.wait()
        return obj.stdout.read()
    except Exception:
        if isNeedPrint:
            print "cmd: %s excute is error" % cmdStr
        return ""


# 阻塞调用,返回执行结果
def sync_excuteCMD_retcode(cmdStr, isNeedPrint = False, isNeedOutput = False):
    if not baseEx.validateString(cmdStr):
        return -1
    try:
        if isNeedOutput:
            obj = subprocess.Popen(cmdStr, shell = True)
        else:
            obj = subprocess.Popen(cmdStr, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        obj.wait()
        return obj.returncode
    except Exception:
        if isNeedPrint:
            print "cmd: %s excute is error" % cmdStr
        return -1


# 阻塞调用,返回执行结果和输出结果
def sync_excuteCMD_all(cmdStr, isNeedPrint = False):
    if not baseEx.validateString(cmdStr):
        return None
    try:
        obj = subprocess.Popen(cmdStr, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        obj.wait()
        return tuple(obj.returncode, obj.stdout.read())
    except Exception:
        if isNeedPrint:
            print "cmd: %s excute is error" % cmdStr
        return None

# 异步执行命令,无法获取任何信息
def async_excute(cmdStr, isNeedPrint = False, isNeedOutput = False):
    if not baseEx.validateString(cmdStr):
        return -1
    try:
        if isNeedOutput:
            subprocess.Popen(cmdStr, shell = True)
        else:
            subprocess.Popen(cmdStr, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        return 0
    except Exception:
        if isNeedPrint:
            print "cmd: %s excute is error" % cmdStr
        return -1
