# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #


"""
说明区:
    请使用命令: python JDiOSUUIDDayToDay.py
    请将需要对比的文件夹写入global_file_dir_path_list中
    之后将输出各个文件夹的uuid去重数
    以及两两对比重复结果
"""
import os
import sys
import CJFKit

# 把需要参加对比的文件夹路径都放在这个数组里
global_file_dir_path_list = ["../iPad_390_1125/parser","../iPad_390_1126/parser","../iPad_390_1127/parser"]

if not CJFKit.validateList(global_file_dir_path_list):
    print "Error: global_file_dir_path_list is empty!"
    sys.exit(-1)

print "--------------  dir collect --------------"
global_file_dir_path_list = set(global_file_dir_path_list)

# 每天的uuid都在其中,每天是一个set。名字记录在下方的list中
global_day_uuid_list = []
global_validate_day_list = []
for file_dir_path in global_file_dir_path_list:
    if os.path.isdir(file_dir_path):
        json_file_list = CJFKit.recursionGetSpecialFilesInSpecialDir(file_dir_path, "*.json")
        json_uuid_list = []
        if CJFKit.validateList(json_file_list):
            for fileName in json_file_list:
                uuid = fileName[0:40]
                json_uuid_list.append(uuid)
            json_uuid_set = set(json_uuid_list)
            global_day_uuid_list.append(json_uuid_set)
            global_validate_day_list.append(file_dir_path)
            print "%s uuid:%d, unique uuid:%d" % (file_dir_path,len(json_uuid_list),len(json_uuid_set))
        else:
            print "%s uuid:0" % file_dir_path


print "\n\n--------------  repetition udid  --------------"

for index1 in range(0,len(global_day_uuid_list) - 1):
    index1_uuid_set = global_day_uuid_list[index1]
    for index2 in range(index1 + 1,len(global_day_uuid_list)):
        index2_uuid_set = global_day_uuid_list[index2]
        repetitionSet = index1_uuid_set & index2_uuid_set
        print "\n ---- Day To Day ---"
        print "Day1: %s" % global_validate_day_list[index1]
        print "Day2: %s\n" % global_validate_day_list[index2]
        if isinstance(repetitionSet,set) and len(repetitionSet) > 0:
            print "repetition udid count:%d" % len(repetitionSet)
            for re_uuid in repetitionSet:
                print re_uuid
        else:
            print "No repetition udid"
