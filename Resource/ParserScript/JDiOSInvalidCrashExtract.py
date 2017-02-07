# -*- coding: utf-8 -*-
# Author by 程剑锋
# Contact on :程剑锋
# Any question please contact with me by Email: chengjianfeng@jd.com
# -------------------- Code Start -------------------- #

"""
说明区:
    提取无效报告,生成json数组,交由后台处理
"""

import CJFKit
import os
import sys


global_file_dir_name = "../iPad_393_AS_1215_16_17/sortOut/crash_symbol/pre_all_fup"
global_output_fileName = global_file_dir_name + "_countResult"

json_file_list = CJFKit.recursionGetSpecialFilesInSpecialDir(global_file_dir_name, "*.json", True)
json_result_list = []

if not CJFKit.validateList(json_file_list):
    print "Error: no json files"
    sys.exit(-1)

for filePath in json_file_list:
    crash_json = CJFKit.safeGetFileContentJSON(filePath)
    crash_create_time_str = CJFKit.safeGetElement(crash_json, [3, "serverUserInfo", "createTime"])
    crash_upload_time_str = CJFKit.safeGetElement(crash_json, [3, "serverUserInfo", "uploadTime"])
    crash_uuid_str = CJFKit.safeGetElement(crash_json, [3, "serverUserInfo", "uuid"])
    if CJFKit.validateString(crash_create_time_str) and CJFKit.validateString(
            crash_upload_time_str) and CJFKit.validateString(crash_uuid_str):
        crash_result_dic = {"createTime":crash_create_time_str, "uploadTime":crash_upload_time_str,
                            "uuid":crash_uuid_str}
        json_result_list.append(crash_result_dic)
    else:
        print "Error: %s serverUserInfo data error" % (os.path.basename(filePath))

if CJFKit.validateList(json_result_list):
    CJFKit.safeWriteFileContentJSON(global_output_fileName, json_result_list)
    print "output file in %s, count : %d ." % (global_output_fileName, len(json_result_list))
else:
    print "json_result_list is empty ."
