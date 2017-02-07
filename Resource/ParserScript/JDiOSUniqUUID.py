# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #


"""
说明区:
    对指定文件夹下的UUID进行去重处理
"""
import os
import sys
import CJFKit

# 把需要参加统计的文件夹路径都放在这个数组里
global_file_dir_path_list = ["../iPad_390_1125/parser","../iPad_390_1126/parser"]

if not CJFKit.validateList(global_file_dir_path_list):
    print "Error: global_file_dir_path_list is empty!"
    sys.exit(-1)

print "--------------  check dir  --------------"
global_file_dir_path_list = set(global_file_dir_path_list)
for dirPath in global_file_dir_path_list:
    print dirPath

print "\n--------------  repetition udid  --------------"

global_uuid_list = []
for file_dir_path in global_file_dir_path_list:
    if os.path.isdir(file_dir_path):
        json_file_list = CJFKit.recursionGetSpecialFilesInSpecialDir(file_dir_path, "*.json")
        if CJFKit.validateList(json_file_list):
            for fileName in json_file_list:
                uuid = fileName[0:40]
                global_uuid_list.append(uuid)

global_uuid_set = set(global_uuid_list)
for uuidName in global_uuid_set:
    count = global_uuid_list.count(uuidName)
    if count > 1:
        print "%s : %d" % (uuidName, count)

print "\n--------------  collect  --------------"
print "all file count : %d" % len(global_uuid_list)
print "uniqueness udid count : %d" % len(global_uuid_set)
