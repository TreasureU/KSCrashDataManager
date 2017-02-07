//
//  CJFInitManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/22.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFInitManager.h"

static NSString* const cjf_init_environment_key = @"cjf_init_environment_key";
static NSString* const cjf_init_environment_value = @"20170113_1331";

@implementation CJFInitManager

+(CJFInitManager*)sharedManager
{
    static CJFInitManager* _sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedManager = [[CJFInitManager alloc] init];
    });
    return _sharedManager;
}

-(void)InitEnvironment
{
    if( SetInitDir(CJFWORKKIT_DIRNAME) ){
        [self buildEnvironment];
        [[NSUserDefaults standardUserDefaults] setObject:cjf_init_environment_value forKey:cjf_init_environment_key];
    }else{
        NSString* init_flag = [[NSUserDefaults standardUserDefaults] stringForKey:cjf_init_environment_key];
        if( !validateString(init_flag) || ![cjf_init_environment_value isEqualToString:init_flag] ){
            [self buildEnvironment];
            [[NSUserDefaults standardUserDefaults] setObject:cjf_init_environment_value forKey:cjf_init_environment_key];
        }
    }
}

-(void)forceDsymFileReplace
{
#ifndef CJF_USE_SELF    //自己的代码不需要替换dsym
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"SourceSymbol/self"]);
#endif
}

-(void)forceScriptFileReplace
{
#ifndef CJF_USE_SELF    //自己的代码不需要替换脚本
    //删除整个脚本文件夹
    removeFileWitName(@"ParserScript");
    //重建脚本文件夹
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/backUp"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/cache"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/CJFKit"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/setting"]);
    
    //重建脚本文件
    //backUp
    copyBundleFileToDocument(@"JDiOSOOMClassify", @"py", @"ParserScript/backUp");
    copyBundleFileToDocument(@"JDiPadAllCrashClassify", @"py", @"ParserScript/backUp");
    copyBundleFileToDocument(@"JDiPadAllCrashConvert", @"py", @"ParserScript/backUp");
    copyBundleFileToDocument(@"JDiPadAllCrashParser", @"py", @"ParserScript/backUp");
    copyBundleFileToDocument(@"JDiPadOneCrashLogParse", @"py", @"ParserScript/backUp");
    
    //cache
    copyBundleFileToDocument(@"systemCache", @"", @"ParserScript/cache");
    
    //setting
    copyBundleFileToDocument(@"filterKeyWordMappingiPad", @"json", @"ParserScript/setting");
    copyBundleFileToDocument(@"filterKeyWordMappingiPhone", @"json", @"ParserScript/setting");
    copyBundleFileToDocument(@"NavAndUrlSortiPad", @"json", @"ParserScript/setting");
    copyBundleFileToDocument(@"NavAndUrlSortiPhone", @"json", @"ParserScript/setting");
    copyBundleFileToDocument(@"systemKeyWordMappingiPad", @"json", @"ParserScript/setting");
    copyBundleFileToDocument(@"systemKeyWordMappingiPhone", @"json", @"ParserScript/setting");
    
    //CJFKit
    copyBundleFileToDocument(@"__init__", @"py", @"ParserScript/CJFKit");
    copyBundleFileToDocument(@"baseEx", @"py", @"ParserScript/CJFKit");
    copyBundleFileToDocument(@"fileEx", @"py", @"ParserScript/CJFKit");
    copyBundleFileToDocument(@"computeEx", @"py", @"ParserScript/CJFKit");
    copyBundleFileToDocument(@"crashSortModel", @"py", @"ParserScript/CJFKit");
    copyBundleFileToDocument(@"timeEx", @"py", @"ParserScript/CJFKit");
    
    //执行脚本
    copyBundleFileToDocument(@"JDiOSRepetitionReportCheck", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSUUIDDayToDay", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDDataContentFilter", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSInvalidCrashExtract", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSUniqUUID", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSAllCrashConvertMutilProcess", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSCrashSortOutFinal", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSCrashSortOutInit", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSCrashSortOutRecursion", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSExcelFromDir", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSNAV_URLSort", @"py", @"ParserScript");
    copyBundleFileToDocument(@"JDiOSOOMFilter", @"py", @"ParserScript");
    
#endif
}

-(void)buildEnvironment
{
    SetInitDir(CJFWORKKIT_DIRNAME);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"Setting"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"LocalCrashData"]);
    
    //重建脚本文件夹
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/backUp"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/cache"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/CJFKit"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"ParserScript/setting"]);
    
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"SourceSymbol"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"SourceSymbol/self"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"SourceSymbol/armv7"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"SourceSymbol/arm64"]);
    SetInitDir([CJFWORKKIT_DIRNAME stringByAppendingPathComponent:@"SourceSymbol/armv7s"]);
    
#ifndef CJF_USE_SELF
    //Script
    [self forceScriptFileReplace];
    
    //SourceSymbol
    [self forceDsymFileReplace];
#endif
}

-(void)rebuildEnvironment
{
#ifndef CJF_USE_SELF
    //删除整个文件夹
    removeFileWitName(@"");
    [self buildEnvironment];
#endif
}



@end
