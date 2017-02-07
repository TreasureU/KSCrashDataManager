//
//  GetRemoteCrashDataManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/25.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "GetRemoteCrashDataManager.h"
#import "CJFNetworkManager.h"

//文件已废弃

NSString* const JDCrashGetAccountKey = @"JDCrashGetAccountKey";
NSString* const JDCrashGetPasswordKey = @"JDCrashGetPasswordKey";

static NSString* const cjf_adminAccount = @"xxxxxxxx";
static NSString* const cjf_adminPassword = @"xxxxxxx";

@implementation GetRemoteCrashDataManager

/*
 {
 @"client":@"apple",
 @"clientVersion":@"5.5.0"
 @"build":@"125580",
 @"uuid":@"781240120912480128312",
 @"pin":@"673302055",
 @"partner":@"pp601",
 @"startTime":@"",
 @"endTime":@"",
 @"fileName":@"iPhone_550_PP3"
 }
 */
+(void)getOperationCookie:(NSDictionary*)paramDic andVC:(id<GetRemoteCrashDataManagerVCDelegate>)crashVC
{
    [GetRemoteCrashDataManager getOperationCookie:paramDic andVC:crashVC withCompleteBlock:nil];
}

+(void)getOperationCookie:(NSDictionary*)paramDic withCompleteBlock:(void(^)(BOOL suc))completeBlock
{
    [GetRemoteCrashDataManager getOperationCookie:paramDic andVC:nil withCompleteBlock:completeBlock];
}

+(void)getOperationCookie:(NSDictionary*)paramDic andVC:(id<GetRemoteCrashDataManagerVCDelegate>)crashVC withCompleteBlock:(void(^)(BOOL suc))completeBlock
{
    if( !validateDictionary(paramDic) ){
        NSLog(@"参数错误.");
        crashVC.logText.string = [crashVC.logText.string stringByAppendingString:@"账户密码校验失败。\n"];
        if( completeBlock ){
            dispatch_async(dispatch_get_main_queue(), ^{
                completeBlock(NO);
            });
        }
        return;
    }
    NSString* adminAccount = cjf_adminAccount;
    NSString* adminPassword = cjf_adminPassword;
    if( validateString([[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetAccountKey]) && validateString([[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetPasswordKey]) ){
        adminAccount = [[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetAccountKey];
        adminPassword = [[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetPasswordKey];
    }
    [CJFNetworkManager clearAllCookies];
    //网络代码已全部废弃
}

+(void)getCrashFileTXT:(NSDictionary*)paramDic andVC:(id<GetRemoteCrashDataManagerVCDelegate>)crashVC withCompleteBlock:(void(^)(BOOL suc))completeBlock

{
    CJFNetworkManager *manager = [[CJFNetworkManager sharedClient] setHttpHeader:CJFNetworkCrashQuery];
    NSDictionary* param = @{@"client":toValidateString(paramDic[@"client"]),
                            @"clientVersion":toValidateString(paramDic[@"clientVersion"]),
                            @"build":toValidateString(paramDic[@"build"]),
                            @"uuid":toValidateString(paramDic[@"uuid"]),
                            @"pin":toValidateString(paramDic[@"pin"]),
                            @"partner":toValidateString(paramDic[@"partner"]),
                            @"bisType":@"",
                            @"msgType":@"1",
                            @"uploadType":@"2",
                            @"exportType":@"2",
                            @"exceptionpage":@"",
                            @"exceptionTypeName":@"",
                            @"exceptionCodeline":@"",
                            @"queryTimeType":@"0",
                            @"startTime":toValidateString(paramDic[@"startTime"]),
                            @"endTime":toValidateString(paramDic[@"endTime"])};
    __weak id<GetRemoteCrashDataManagerVCDelegate> weakCrashVC = crashVC;
    [manager POST:CRASH_DATA_DOWNLOAD parameters:param progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
        NSString *contentStr = [[NSString alloc] initWithData:responseObject encoding:NSUTF8StringEncoding];
        if( validateString(contentStr) ){
            NSInteger count = [contentStr subStringCount:@"\n"];
            if( contentStr.length > 0 ){
                count ++;
            }
            NSLog(@"拉取到crash数据： %ld 条",count);
            weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:[NSString stringWithFormat:@"拉取到crash数据： %ld 条",count]];
            
            NSString* fileName = toValidateString(paramDic[@"fileName"]);
            if( !validateString(fileName) ){
                fileName = [NSString stringWithFormat:@"crash_%@.txt",[[NSDate date] month_day_hours_minutes_seconds]];
            }
            if( ![fileName hasSuffix:@".txt"] ){
                fileName = [fileName stringByAppendingString:@".txt"];
            }
            NSError* error = nil;
            BOOL ret = [contentStr writeToFile:getFilePath([@"LocalCrashData/" stringByAppendingString:fileName]) atomically:YES encoding:NSUTF8StringEncoding error:&error];
            if( error == nil && ret ){
                if( completeBlock ){
                    dispatch_async(dispatch_get_main_queue(), ^{
                        completeBlock(YES);
                    });
                }
                NSLog(@"crash数据写入成功");
                weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash数据写入成功"]];
            }else{
                if( completeBlock ){
                    dispatch_async(dispatch_get_main_queue(), ^{
                        completeBlock(NO);
                    });
                }
                NSLog(@"crash数据写入失败");
                weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash数据写入失败"]];
            }
        }else{
            NSLog(@"暂无crash数据");
            weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:@"暂无crash数据。\n"];
            if( completeBlock ){
                dispatch_async(dispatch_get_main_queue(), ^{
                    completeBlock(NO);
                });
            }
            return;
        }
    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
        NSLog(@"打开crash查询页面失败");
        weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:@"打开crash查询页面失败。\n"];
        if( completeBlock ){
            dispatch_async(dispatch_get_main_queue(), ^{
                completeBlock(NO);
            });
        }
        return;
    }];
}

#pragma mark - 废弃接口
//页面爬虫抓取方式
//-(void)getCrashFile:(CrashViewController*)crashVC
//{
//    __weak __typeof(CrashViewController*) weakCrashVC = crashVC;
//    CJFNetworkManager *manager = [[CJFNetworkManager sharedClient] setHttpHeader:CJFNetworkCrashQuery];
//    NSDictionary* param = @{@"client":toValidateString(weakCrashVC.clientChoiceBtn.selectedItem.title),
//                            @"clientVersion":toValidateString(weakCrashVC.versionLab.stringValue),
//                            @"buildCode":toValidateString(weakCrashVC.buildLab.stringValue),
//                            @"uuid":toValidateString(weakCrashVC.UUIDLab.stringValue),
//                            @"pin":toValidateString(weakCrashVC.userNameLab.stringValue),
//                            @"partner":toValidateString(weakCrashVC.pipeLab.stringValue),
//                            @"bisType":@"",
//                            @"msgType":@"1",
//                            @"uploadType":@"-1",
//                            @"exportType":@"2",
//                            @"exceptionpage":@"",
//                            @"exceptionTypeName":@"",
//                            @"exceptionCodeline":@"",
//                            @"queryTimeType":@"0",
//                            @"pageSize":@"1000",
//                            @"startTime":toValidateString(weakCrashVC.crashStartLab.stringValue),
//                            @"endTime":toValidateString(weakCrashVC.crashEndLab.stringValue)};
//    [manager POST:CRASH_DATA_QUERY parameters:param progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
//        NSString *contentStr = [[NSString alloc] initWithData:responseObject encoding:NSUTF8StringEncoding];
//        NSArray* hrefAllArr = [contentStr componentsSeparatedFromString:@"<a href=\"" toString:@"\">"];
//        NSMutableArray* hrefCrashhArr = [[NSMutableArray alloc] initWithCapacity:10];
//        for (NSString* href in hrefAllArr) {
//            if( validateString(href) && [href containsString:@"exceptioninfo.action?id="] ){
//                [hrefCrashhArr addObject:[NSString stringWithFormat:@"%@%@",CRASH_DATA_DETAIL_Pre,href]];
//            }
//        }
//        if( validateArray(hrefCrashhArr) ){
//            NSLog(@"拉取到crash数据： %ld 条",hrefCrashhArr.count);
//            weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:[NSString stringWithFormat:@"拉取到crash数据： %ld 条",hrefCrashhArr.count]];
//            
//            NSString* fileDirName = toValidateString(weakCrashVC.fileNameLab.stringValue);
//            if( !validateString(fileDirName) ){
//                fileDirName = [[NSDate date] year_month_day_hours_minutes_seconds_msec];
//            }
//            //一定会新建文件夹，如果重名会创建副本文件
//            NSString* sourceDirName = [fileDirName stringByAppendingPathComponent:@"source"];
//            //预创建多个文件夹
//            sourceDirName = CreatDirAndNotRemove( sourceDirName );
//            NSLog(@"新建crash文件夹：%@",fileDirName);
//            weakCrashVC.logText.string = [weakCrashVC.logText.string stringByAppendingString:[NSString stringWithFormat:@"新建crash文件夹：%@。\n",fileDirName]];
//            
//            for (NSString* crashHref in hrefCrashhArr) {
//                dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
//                    [weakCrashVC getCrashDetail:crashHref andFileDir:sourceDirName];
//                });
//            }
//        }else{
//            NSLog(@"暂无crash数据");
//            weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:@"暂无crash数据。\n"];
//            return;
//        }
//    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
//        NSLog(@"打开crash查询页面失败");
//        weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:@"打开crash查询页面失败。\n"];
//        return;
//    }];
//}
//
////页面爬虫抓取方式
//-(void)getCrashDetail:(NSString*)urlAddress andFileDir:(NSString*)dirName
//{
//    if( !validateString(urlAddress) || !validateString(dirName) ){
//        return;
//    }
//    __weak __typeof(self) weakSelf = self;
//    CJFNetworkManager *manager = [[CJFNetworkManager sharedClient] setHttpHeader:CJFNetworkCrashDetail];
//    [manager GET:urlAddress parameters:nil progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id  _Nullable responseObject) {
//        NSString *contentStr = [[NSString alloc] initWithData:responseObject encoding:NSUTF8StringEncoding];
//        
//        //文件名获取操作，目前采用创建时间作为依据
//        //对于软链接来说存在问题，更换为唯一ID
//        //        NSString* createTime = nil;
//        //        NSArray* createTimeArr = [contentStr componentsSeparatedFromString:@"<td align=\"right\" width=\"120\"> 创建时间：</td>" toString:@"</tr>"];
//        //        if( validateArray(createTimeArr) ){
//        //            createTime = createTimeArr[0];
//        //            createTimeArr = [createTime componentsSeparatedFromString:@"<td>" toString:@"</td>"];
//        //            if( validateArray(createTimeArr) ){
//        //                createTime = [createTimeArr[0] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
//        //            }
//        //        }
//        
//        //文件内容获取操作
//        NSArray* contentArr = [contentStr componentsSeparatedFromString:@"<textarea rows=\"10\" cols=\"100\">" toString:@"</textarea>"];
//        NSString* crashStr = nil;
//        if( validateArray(contentArr) ){
//            crashStr = contentArr[0];
//        }
//        if( validateString(crashStr) ){
//            
//            //文件名获取操作，目前采用后台唯一ID作为依据
//            NSString* fileName = nil;
//            NSArray* fileNameArr = [urlAddress componentsSeparatedFromString:@"exceptioninfo.action?id=" toString:@"&aura="];
//            if( validateArray(fileNameArr) ){
//                fileName = fileNameArr[0];
//            }else{
//                fileName = [NSString randomLengthString:24];
//            }
//            
//            //文件名获取操作，目前采用创建时间作为依据
//            //对于软链接来说存在问题，更换为唯一ID
//            //            NSString* fileName = nil;
//            //            if( !validateString(createTime) ){
//            //                fileName = [NSString stringWithFormat:@"%u",arc4random_uniform(10000000)];
//            //            }else{
//            //                fileName = [NSString stringWithFormat:@"%@_%u",createTime,arc4random_uniform(10000000)];
//            //            }
//            
//            //文件名拼接操作，必须保留
//            fileName = [fileName stringByAppendingString:@".json"];
//            fileName = [dirName stringByAppendingString:[NSString stringWithFormat:@"/%@",fileName]];
//            
//            //分裂字符串操作
//            NSError* err = nil;
//            BOOL success = NO;
//            crashStr = [crashStr SplitStringToEnd:@"||" withCount:2];
//            if( !crashStr ){
//                NSLog(@"crash split error: %@",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash split error: %@",urlAddress]];
//                return;
//            }
//            
//            //解压缩+AES解密操作
//            NSData* crashDecodeData = [crashStr dataUsingEncoding:NSUTF8StringEncoding];
//            crashDecodeData = [Base64 decodeData:crashDecodeData];
//            NSString* key = [@"NSObject" stringByAppendingString:@"NSString"];
//            crashDecodeData = [JDGzip aes256DecryptWithData:crashDecodeData key:[key dataUsingEncoding:NSUTF8StringEncoding] iv:nil];
//            crashDecodeData = [JDGzip gzipInflate:crashDecodeData];
//            if( !crashDecodeData ){
//                NSLog(@"crash decode error: %@",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash decode error: %@",urlAddress]];
//                return;
//            }
//            crashStr = [[NSString alloc] initWithData:crashDecodeData encoding:NSUTF8StringEncoding];
//            
//            //json格式化及校验操作
//            NSDictionary* crashDic =  [NSJSONSerialization JSONObjectWithData:[crashStr dataUsingEncoding:NSUTF8StringEncoding] options:0 error:&err];
//            if( !validateDictionary(crashDic) || err ){
//                NSLog(@"crash format error: %@",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash format error: %@",urlAddress]];
//                return;
//            }
//            NSData* crashData = [NSJSONSerialization dataWithJSONObject:crashDic options:NSJSONWritingPrettyPrinted error:&err];
//            if( !crashData || err ){
//                NSLog(@"crash format error: %@",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash format error: %@",urlAddress]];
//                return;
//            }
//            crashStr = [[NSString alloc] initWithData:crashData encoding:NSUTF8StringEncoding];
//            if( !validateString(crashStr) ){
//                NSLog(@"crash format error: %@",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash format error: %@",urlAddress]];
//                return;
//            }
//            
//            //文件写入操作
//            success = [crashStr writeToFile:fileName atomically:YES encoding:NSUTF8StringEncoding error:&err];
//            if( success && !err ){
//                NSLog(@"crash数据写入成功：%@",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash数据写入成功：%@\n",urlAddress]];
//                return;
//            }else{
//                NSLog(@"crash数据写入出错：%@。",urlAddress);
//                weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash数据写入出错：%@\n",urlAddress]];
//                return;
//            }
//        }else{
//            NSLog(@"crash详情页面数据为空：%@",urlAddress);
//            weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"crash详情页面数据为空：%@\n",urlAddress]];
//            return;
//        }
//    } failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
//        NSLog(@"获取crash详情页面失败：%@",urlAddress);
//        weakSelf.logText.string = [weakSelf.logText.string stringByAppendingString:[NSString stringWithFormat:@"获取crash详情页面失败：%@\n",urlAddress]];
//        return;
//    }];
//}


@end
