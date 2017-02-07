//
//  CJFScriptExecuteManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/23.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFScriptExecuteManager.h"

static NSInteger const CJF_Script_Max_ResultValue = 100;

@interface CJFScriptExecuteManager ()

@property(nonatomic,strong) NSOperationQueue* scriptQueue;
@property(nonatomic,strong) NSMutableDictionary* resultDic;

@end

@implementation CJFScriptExecuteManager

+(CJFScriptExecuteManager*)sharedManager
{
    static CJFScriptExecuteManager* manager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        manager = [[CJFScriptExecuteManager alloc] init];
    });
    return manager;
}

- (instancetype)init
{
    self = [super init];
    if (self) {
        _scriptQueue = [[NSOperationQueue alloc] init];
        _scriptQueue.maxConcurrentOperationCount = 1;
        _scriptQueue.name = @"com.cjf.scriptQueue";
        
        _resultDic = [[NSMutableDictionary alloc] initWithCapacity:10];
    }
    return self;
}

-(NSString*)syncExcuteScript:(CJFScriptType)scriptName andParamDic:(NSDictionary*)paramDic
{
    @weakify(self);
    NSString* resultKey = [self getResultKey];
    dispatch_semaphore_t semaphore;
    switch (scriptName) {
        case CJFScriptParser:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* version = toValidateString(paramDic[@"version"]);
            NSString* build = toValidateString(paramDic[@"build"]);
            NSString* dsymFileName = toValidateString(paramDic[@"dsymFileName"]);
            NSString* limitFunc = toValidateString(paramDic[@"limitFunc"]);
            NSString* grayFlagStr = toValidateString(paramDic[@"grayFlagStr"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(version) && validateString(build) && validateString(dsymFileName) && validateString(limitFunc) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSAllCrashConvertMutilProcess.py %@ ../%@ %@ %@ %@ %@ %@",appName,selectedFile,version,build,dsymFileName,limitFunc,grayFlagStr]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptClassifyInit:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutInit.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptClassifyRecursion:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutRecursion.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptClassifyFinal:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutFinal.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptOOMClassify:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* sourceDir = toValidateString(paramDic[@"sourceDir"]);
            NSString* targetDir = toValidateString(paramDic[@"targetDir"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(sourceDir) && validateString(targetDir)){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSNAV_URLSort.py %@ ../%@ %@ %@",appName,selectedFile,sourceDir,targetDir]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptQuicklyCount:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSOOMFilter.py %@ ../%@",appName,selectedFile]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptExcel:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* pathStr = toValidateString(paramDic[@"pathStr"]);
            if( validateString(appName) && validateString(pathStr) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSExcelFromDir.py %@ %@",appName,pathStr]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptNAV_URL:
        {
            if( !validateDictionary(paramDic) ){
                return nil;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* sourceDir = toValidateString(paramDic[@"sourceDir"]);
            NSString* targetDir = toValidateString(paramDic[@"targetDir"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(sourceDir) && validateString(targetDir) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSNAV_URLSort.py %@ ../%@ %@ %@",appName,selectedFile,sourceDir,targetDir]];
                    [self addResultWithKey:resultKey andValue:result];
                    dispatch_semaphore_signal(semaphore);
                }];
                dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
                return toValidateString([self getResultWithKey:resultKey]);
            }
            return nil;
        }
            break;
        case CJFScriptClassifyGroup:
        {
            NSString* result = [self syncExcuteScript:CJFScriptClassifyInit andParamDic:paramDic];
            if( validateString(result) ){
                NSString* tmp = [self syncExcuteScript:CJFScriptClassifyRecursion andParamDic:paramDic];
                if( validateString(tmp) ){
                    result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                    tmp = [self syncExcuteScript:CJFScriptClassifyFinal andParamDic:paramDic];
                    if( validateString(tmp) ){
                        result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                    }
                }
            }
            return result;
        }
            break;
        case CJFScriptNormalCrashParserGroup:
        {
            NSString* result = [self syncExcuteScript:CJFScriptParser andParamDic:paramDic];
            if( validateString(result) ){
                NSString* tmp = [self syncExcuteScript:CJFScriptClassifyGroup andParamDic:paramDic];
                if( validateString(tmp) ){
                    result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                }
            }
            return result;
        }
            break;
        default:
            return nil;
    }
}

-(BOOL)asyncExcuteScript:(CJFScriptType)scriptName andParamDic:(NSDictionary*)paramDic withCompleteBlock:(void (^)(NSString* result))completeBlock
{
    @weakify(self);
    switch (scriptName) {
        case CJFScriptParser:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* version = toValidateString(paramDic[@"version"]);
            NSString* build = toValidateString(paramDic[@"build"]);
            NSString* dsymFileName = toValidateString(paramDic[@"dsymFileName"]);
            NSString* limitFunc = toValidateString(paramDic[@"limitFunc"]);
            NSString* grayFlagStr = toValidateString(paramDic[@"grayFlagStr"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(version) && validateString(build) && validateString(dsymFileName) && validateString(limitFunc) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSAllCrashConvertMutilProcess.py %@ ../%@ %@ %@ %@ %@ %@",appName,selectedFile,version,build,dsymFileName,limitFunc,grayFlagStr]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptClassifyInit:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutInit.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptClassifyRecursion:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutRecursion.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptClassifyFinal:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutFinal.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptOOMClassify:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* sourceDir = toValidateString(paramDic[@"sourceDir"]);
            NSString* targetDir = toValidateString(paramDic[@"targetDir"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(sourceDir) && validateString(targetDir)){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSNAV_URLSort.py %@ ../%@ %@ %@",appName,selectedFile,sourceDir,targetDir]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptQuicklyCount:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSOOMFilter.py %@ ../%@",appName,selectedFile]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptExcel:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* pathStr = toValidateString(paramDic[@"pathStr"]);
            if( validateString(appName) && validateString(pathStr) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSExcelFromDir.py %@ %@",appName,pathStr]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptNAV_URL:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* sourceDir = toValidateString(paramDic[@"sourceDir"]);
            NSString* targetDir = toValidateString(paramDic[@"targetDir"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(sourceDir) && validateString(targetDir) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSNAV_URLSort.py %@ ../%@ %@ %@",appName,selectedFile,sourceDir,targetDir]];
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptClassifyGroup:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutInit.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                    if( validateString(result) ){
                        NSString* tmp = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutRecursion.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                        if( validateString(tmp) ){
                            result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                            tmp = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutFinal.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                            if( validateString(tmp) ){
                                result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                            }
                        }
                    }
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        case CJFScriptNormalCrashParserGroup:
        {
            if( !validateDictionary(paramDic) ){
                return NO;
            }
            NSString* appName = toValidateString(paramDic[@"appName"]);
            NSString* selectedFile = toValidateString(paramDic[@"selectedFile"]);
            NSString* version = toValidateString(paramDic[@"version"]);
            NSString* build = toValidateString(paramDic[@"build"]);
            NSString* dsymFileName = toValidateString(paramDic[@"dsymFileName"]);
            NSString* limitFunc = toValidateString(paramDic[@"limitFunc"]);
            NSString* grayFlagStr = toValidateString(paramDic[@"grayFlagStr"]);
            NSString* compareDirName = toValidateString(paramDic[@"compareDirName"]);
            if( validateString(appName) && validateString(selectedFile) && validateString(version) && validateString(build) && validateString(dsymFileName) && validateString(limitFunc) && validateString(compareDirName) ){
                [self.scriptQueue addOperationWithBlock:^{
                    @strongify(self);
                    NSString* result = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSAllCrashConvertMutilProcess.py %@ ../%@ %@ %@ %@ %@ %@",appName,selectedFile,version,build,dsymFileName,limitFunc,grayFlagStr]];
                    if( validateString(result) ){
                        NSString* tmp = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutInit.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                        if( validateString(tmp) ){
                            result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                            tmp = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutRecursion.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                            if( validateString(tmp) ){
                                result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                                tmp = [self runScriptInMainDir:[NSString stringWithFormat:@"python ./JDiOSCrashSortOutFinal.py %@ ../%@ ../%@",appName,selectedFile,compareDirName]];
                                if( validateString(tmp) ){
                                    result = [NSString stringWithFormat:@"%@\n%@",result,tmp];
                                }
                            }
                        }
                    }
                    dispatch_async(dispatch_get_main_queue(), ^{
                        if( completeBlock ){
                            completeBlock(result);
                        }
                    });
                }];
                return YES;
            }
            return NO;
        }
            break;
        default:
            return NO;
    }
}

#pragma mark - 私有方法

-(NSString*)getResultKey
{
    static int keyValue = 0;
    @synchronized (self) {
        if( keyValue == CJF_Script_Max_ResultValue ){
            keyValue = 0;
        }
        return [NSString stringWithFormat:@"%d",keyValue++];
    }
}

-(BOOL)addResultWithKey:(NSString*)key andValue:(NSString*)value
{
    if( validateString(key) ){
        @synchronized (self) {
            self.resultDic[key] = toValidateString(value);
        }
        return YES;
    }
    return NO;
}

-(NSString*)getResultWithKey:(NSString*)key
{
    if( validateString(key) ){
        @synchronized (self) {
            return toValidateString(self.resultDic[key]);
        }
    }
    return @"";
}

-(NSString*)runScriptInMainDir:(NSString*)cmd
{
    if( validateString(cmd) ){
        return toValidateString(runSystemCommand(cmd, [NSString stringWithFormat:@"%@/ParserScript",getMainDocumentDirPath()]));
    }
    return @"";
}

@end
