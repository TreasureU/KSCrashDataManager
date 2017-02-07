//
//  CJFCrashDataReadManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/27.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFCrashDataReadManager.h"
#import "CJFFileReader.h"

@interface CJFCrashDataReadManager ()

@property(nonatomic,strong) CJFFileReader* fileReader;
@property(nonatomic,strong) NSMutableDictionary* userInfoDic;

@end

@implementation CJFCrashDataReadManager

+(CJFCrashDataReadManager*)getManager
{

    return [[CJFCrashDataReadManager alloc] init];
}

- (instancetype)init
{
    self = [super init];
    if (self) {
        _userInfoDic = [[NSMutableDictionary alloc] initWithCapacity:10];
    }
    return self;
}


- (BOOL)startReadCrashData:(NSDictionary*)paramDic andReadVC:(id<CJFCrashDataReadManagerDelegate>)readVC
{
    return [self startReadCrashData:paramDic andReadVC:readVC withCompleteBlock:nil];
}

- (BOOL)startReadCrashData:(NSDictionary*)paramDic withCompleteBlock:(void(^)(BOOL suc))completeBlock
{
    return [self startReadCrashData:paramDic andReadVC:nil withCompleteBlock:completeBlock];
}

- (BOOL)startReadCrashData:(NSDictionary*)paramDic andReadVC:(id<CJFCrashDataReadManagerDelegate>)readVC withCompleteBlock:(void(^)(BOOL suc))completeBlock
{
    if( !validateDictionary(paramDic) ){
        if( completeBlock ){
            dispatch_async(dispatch_get_main_queue(), ^{
                completeBlock(NO);
            });
        }
        return NO;
    }
    [self.userInfoDic removeAllObjects];
    
    NSString* selectedFile = toValidateString(paramDic[@"chooseFile"]);
    NSString* appName = toValidateString(paramDic[@"appName"]);
    NSString* targetDirName = toValidateString(paramDic[@"targetDirName"]);
    if( !validateString(targetDirName) ){
        targetDirName = [[NSDate date] year_month_day_hours_minutes_seconds_msec];
    }
    if( validateString(appName) && validateString(selectedFile) && validateString(targetDirName) ){
        if( [[NSFileManager defaultManager] fileExistsAtPath:getFilePath(targetDirName)] ){
            removeFileWitName(targetDirName);
        }
        targetDirName = CreatDirAndNotRemove(targetDirName);
        NSString* rootDirName = targetDirName;
        [[NSFileManager defaultManager] createDirectoryAtPath:[targetDirName stringByAppendingPathComponent:@"source"] withIntermediateDirectories:YES attributes:nil error:nil];
        targetDirName = [targetDirName stringByAppendingPathComponent:@"source"];
        self.fileReader = [[CJFFileReader alloc] initWithLocalFilePath:getFilePath([@"LocalCrashData" stringByAppendingPathComponent:selectedFile])];
        NSString* tip = @"文件正在提取中，请稍后.......";
        NSLog(@"%@",tip);
        [readVC willAppendLog:tip];
        __weak __typeof(self) weakSelf = self;
        [self.fileReader enumerateLinesUsingBlock:^(NSInteger lineNumber, NSString *line) {
            //处理单行数据
            
            /*
             0 上传方式（0-老版,1-pl,2-ks）；
             1 崩溃上报时间；
             2 崩溃创建时间；
             3 平台；
             4 客户端版本；
             5 build；
             6 pin；
             7 uuid；
             8 品牌；
             9 型号；
             10 屏幕；
             11 渠道；
             12 操作系统版本；
             13 异常类型；
             14 异常代码行；
             15 堆栈；
             16 异常页面信息；
             17异常停留页面
             (
             "2016-08-26 15:56:44",------>1.崩溃发生时间
             "2016-08-26 18:02:10",------>2.崩溃上报时间
             apple,------>3.平台
             "5.3.0",------>4.客户端版本
             12348,------>5.build ID
             none,------>6.pin
             4dfc7aeab14613e3724dc9f56b179493b88877a7,------>7.uuid
             apple,------>8.品牌
             "iPhone8,1",------>9.型号
             "750*1334",------>10.屏幕大小
             apple,------>11.渠道
             "9.3.4",------>12.操作系统版本
             nsexception,------>13.崩溃类型
             "Application threw exception NSInvalidArgumentException: (null)Originated at or in a subcall of -[NewMoreViewController gotoNextPageWithModel:]",------>14.崩溃原因
             exceed,------>15.崩溃具体信息
             none------>16.异常页面信息
             )*/
            __strong __typeof(self) strongSelf = weakSelf;
            //            NSArray* contentList = [line componentsSeparatedFromString:@"<|>" toString:@"<|>"];
            NSArray* contentList = [line componentsSeparatedByString:@"<|>"];
            if( [contentList isKindOfClass:[NSArray class]] && contentList.count >= 15 ){
                NSString* fileName = [contentList objectAtIndex:7];
                if( !validateString(fileName) ){
                    fileName = [NSString randomLengthString:40];
                }
                fileName = [fileName stringByAppendingString:@"_"];
                fileName = [fileName stringByAppendingString:[NSString randomLengthString:8]];
                fileName = [fileName stringByAppendingString:@".json"];
                
                NSDictionary* infoDic = [[self class] convertUserInfo:contentList];
                self.userInfoDic[fileName] = infoDic;
                
                NSString* crashStr = [contentList objectAtIndex:15];
                [strongSelf writeCrashStringToFile:fileName UseCrashStr:crashStr andDirPath:targetDirName];
            }
        } completionBlock:^(NSInteger numberOfLines) {
            NSData* userInfoDicData = [NSJSONSerialization dataWithJSONObject:self.userInfoDic options:NSJSONWritingPrettyPrinted error:nil];
            NSString* userInfoDicStr = [[NSString alloc] initWithData:userInfoDicData encoding:NSUTF8StringEncoding];
            BOOL suc = [userInfoDicStr writeToFile:[rootDirName stringByAppendingPathComponent:@"userInfoMapping.json"] atomically:YES encoding:NSUTF8StringEncoding error:nil];
            
            if( suc ){
                NSString* tip = @"用户信息写入成功。";
                NSLog(@"%@",tip);
                [readVC willAppendLog:tip];
            }
            
            if( completeBlock ){
                dispatch_async(dispatch_get_main_queue(), ^{
                    completeBlock(YES);
                });
            }
            
            NSString* tip = @"文件提取已完成。";
            NSLog(@"%@",tip);
            [readVC willAppendLog:tip];
        }];
        return YES;
    }else{
        if( completeBlock ){
            dispatch_async(dispatch_get_main_queue(), ^{
                completeBlock(NO);
            });
        }
        return NO;
    }
}

-(BOOL)writeCrashStringToFile:(NSString*)fileName UseCrashStr:(NSString*)crashStr andDirPath:(NSString*)dirPath
{
    if( !validateString(fileName) ){
        fileName = [NSString randomLengthString:24];
    }
    if( !validateString(dirPath) ){
        return NO;
    }
    if( !validateString(crashStr) ){
        return NO;
    }
    if( ![crashStr isEqualToString:@"exceed"] ){
        //解压缩+AES解密操作
        NSData* crashDecodeData = [crashStr dataUsingEncoding:NSUTF8StringEncoding];
        crashDecodeData = [Base64 decodeData:crashDecodeData];
        NSString* key = [@"NSObject" stringByAppendingString:@"NSString"];
        crashDecodeData = [JDGzip aes256DecryptWithData:crashDecodeData key:[key dataUsingEncoding:NSUTF8StringEncoding] iv:nil];
        crashDecodeData = [JDGzip gzipInflate:crashDecodeData];
        if( !crashDecodeData ){
            return NO;
        }
        crashStr = [[NSString alloc] initWithData:crashDecodeData encoding:NSUTF8StringEncoding];
        
        if( ![crashStr isEqualToString:@"json failure"] ){
            //json格式化及校验操作
            NSError* err = nil;
            NSDictionary* crashDic =  [NSJSONSerialization JSONObjectWithData:[crashStr dataUsingEncoding:NSUTF8StringEncoding] options:0 error:&err];
            //由于此处会存在 Number过大，无法承载的问题，会导致 JSONObjectWithData 出错
            //为了使尽可能的解析更多的crash，选择忽略这一次异常。
            if( validateDictionary(crashDic) &&  !err ){
                NSData* crashData = [NSJSONSerialization dataWithJSONObject:crashDic options:NSJSONWritingPrettyPrinted error:&err];
                if( crashData && !err ){
                    NSString* tmpStr = [[NSString alloc] initWithData:crashData encoding:NSUTF8StringEncoding];
                    if( validateString(crashStr) ){
                        crashStr = tmpStr;
                    }
                }
            }
        }
    }
    
    NSString* filePath = [dirPath stringByAppendingPathComponent:fileName];
    //文件写入操作
    NSError* err = nil;
    BOOL success = NO;
    success = [crashStr writeToFile:filePath atomically:YES encoding:NSUTF8StringEncoding error:&err];
    if( success && !err ){
        return YES;
    }else{
        return NO;
    }
}

+(NSDictionary*)convertUserInfo:(NSArray*)userInfo
{
    /*
     0 上传方式（0-老版,1-pl,2-ks）；
     1 崩溃上报时间；
     2 崩溃创建时间；
     3 平台；
     4 客户端版本；
     5 build；
     6 pin；
     7 uuid；
     8 品牌；
     9 型号；
     10 屏幕；
     11 渠道；
     12 操作系统版本；
     13 异常类型；
     14 异常代码行；
     15 堆栈；
     16 异常页面信息；
     17 异常停留页面
     */
    NSDictionary* dic = @{
                          @"upload":( userInfo.count > 0 ? userInfo[0] : @"none" ),
                          @"uploadTime":( userInfo.count > 1 ? userInfo[1] : @"none" ),
                          @"createTime":( userInfo.count > 2 ? userInfo[2] : @"none" ),
                          @"platform":( userInfo.count > 3 ? userInfo[3] : @"none" ),
                          @"version":( userInfo.count > 4 ? userInfo[4] : @"none" ),
                          @"build":( userInfo.count > 5 ? userInfo[5] : @"none" ),
                          @"pin":( userInfo.count > 6 ? userInfo[6] : @"none" ),
                          @"uuid":( userInfo.count > 7 ? userInfo[7] : @"none" ),
                          @"brand":( userInfo.count > 8 ? userInfo[8] : @"none" ),
                          @"model":( userInfo.count > 9 ? userInfo[9] : @"none" ),
                          @"screen":( userInfo.count > 10 ? userInfo[10] : @"none" ),
                          @"channel":( userInfo.count > 11 ? userInfo[11] : @"none" ),
                          @"osVerison":( userInfo.count > 12 ? userInfo[12] : @"none" ),
                          @"exceptionType":( userInfo.count > 13 ? userInfo[13] : @"none" ),
                          @"exceptionCodeLine":( userInfo.count > 14 ? userInfo[14] : @"none" ),
                          @"stack":( @"please see detail" ),
                          @"exceptionInfo":( userInfo.count > 16 ? userInfo[16] : @"none" ),
                          @"exceptionVC":( userInfo.count > 17 ? userInfo[17] : @"none" )
                          };
    return dic;
}

@end
