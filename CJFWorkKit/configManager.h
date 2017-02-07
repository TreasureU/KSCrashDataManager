//
//  configManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/5/3.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#ifndef configManager_h
#define configManager_h

#ifdef DEBUG
#define TEST_CJFWORKKIT_DEBUG   1
#endif

//全局切换,1表示内部使用，0/不定义表示提供外部使用
//#define CJF_USE_SELF 1

#ifndef CJF_USE_SELF
#define CJFWORKKIT_DIRNAME  @"JDCrashWorkSpace"
#else
#define CJFWORKKIT_DIRNAME  @"CJFWorkKit"
#endif

//Network request URL

#define CRASH_DATA_DOWNLOAD     @"http://bugly.m.jd.com/admin/exception/crashanalysis/OriginalData/exceptionexcel.action?"
//已弃用
#define CRASH_DATA_QUERY        @"http://ccadmin.m.jd.com/admin/exception/list.action"
//已弃用
#define CRASH_DATA_DETAIL_Pre   @"http://ccadmin.m.jd.com/admin/exception/"

//伪装成chrome浏览器
#define CJF_USER_AGENT  @"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36"

#endif /* configManager_h */
