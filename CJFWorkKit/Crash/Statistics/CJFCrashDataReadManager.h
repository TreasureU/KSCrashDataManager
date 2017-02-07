//
//  CJFCrashDataReadManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/27.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol CJFCrashDataReadManagerDelegate <NSObject>

@required
-(void)willAppendLog:( NSString*)appendStr;

@end

@interface CJFCrashDataReadManager : NSObject

+(CJFCrashDataReadManager*)getManager;


/**
 {
    @"appName":@"iPad",
    @"selectedFile":@"",
    @"targetDirName":@""
 }
 */
- (BOOL)startReadCrashData:(NSDictionary*)paramDic andReadVC:(id<CJFCrashDataReadManagerDelegate>)readVC;
- (BOOL)startReadCrashData:(NSDictionary*)paramDic withCompleteBlock:(void(^)(BOOL suc))completeBlock;
- (BOOL)startReadCrashData:(NSDictionary*)paramDic andReadVC:(id<CJFCrashDataReadManagerDelegate>)readVC withCompleteBlock:(void(^)(BOOL suc))completeBlock;

@end
