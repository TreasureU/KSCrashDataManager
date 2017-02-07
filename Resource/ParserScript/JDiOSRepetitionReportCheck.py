# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #


"""
说明区:
    对重复上传的报告进行查询
"""

import os
import CJFKit


# 把需要参加统计的文件夹路径都放在这个数组里
global_file_dir_name = "../iPad_393_AS_1227/source"

json_file_list = CJFKit.recursionGetSpecialFilesInSpecialDir(global_file_dir_name, "*.json")
global_uuid_list = []
for fileName in json_file_list:
    uuid = fileName[0:40]
    global_uuid_list.append(uuid)

global_uuid_set = set(global_uuid_list)
repetition_uuid_list = []
repetition_uuid_dic = {}

for uuidName in global_uuid_set:
    if global_uuid_list.count(uuidName) > 1:
        print "%s : %d" % (uuidName, global_uuid_list.count(uuidName))
        repetition_uuid_list.append(uuidName)
        repetition_uuid_dic[uuidName] = []

# 新建文件夹
global_repetition_dir_path = global_file_dir_name + "_uuid_repetition"
CJFKit.safeCreateDir(global_repetition_dir_path)
for uuid_file_dir_name in repetition_uuid_list:
    CJFKit.safeCreateDir(global_repetition_dir_path + "/" + uuid_file_dir_name)

source_json_path_list = CJFKit.recursionGetSpecialFilesInSpecialDir(global_file_dir_name, "*.json", needPathName = True)
for uuid_file_name in source_json_path_list:
    test_uuid = os.path.basename(uuid_file_name)[0:40]
    if test_uuid in repetition_uuid_list:
        repetition_uuid_dic[test_uuid].append(uuid_file_name)
        CJFKit.safeCopyFileToDir(uuid_file_name, global_repetition_dir_path + "/" + test_uuid)

print "\n\n"

problem_file_list = []

for uuid_rep_key in repetition_uuid_dic:
    uuid_rep_list = repetition_uuid_dic[uuid_rep_key]
    isHave = False
    count = len(uuid_rep_list)
    for i in range(0, count - 2):
        countTwo = i + 1
        for j in range(countTwo, count - 1):
            str1 = CJFKit.safeGetFileContentStr(uuid_rep_list[i])
            str2 = CJFKit.safeGetFileContentStr(uuid_rep_list[j])
            if str1 == str2:
                problem_file_list.append(uuid_rep_list[i])
                problem_file_list.append(uuid_rep_list[j])
                print "%s == %s" % (os.path.basename(uuid_rep_list[i]), os.path.basename(uuid_rep_list[j]))
                isHave = True
    if isHave:
        print "----------- %s ----------- end\n\n" % uuid_rep_key

problem_file_list = set(problem_file_list)

print "\n--------------  collect  --------------"
print "all file count : %d" % len(global_uuid_list)
print "uniqueness udid count : %d" % len(global_uuid_set)
print "repetition file count : %d" % len(problem_file_list)
