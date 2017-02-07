//
//  GetRemoteCrashDataManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/25.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

extern NSString* const JDCrashGetAccountKey;
extern NSString* const JDCrashGetPasswordKey;

@protocol GetRemoteCrashDataManagerVCDelegate <NSObject>

@required
@property (unsafe_unretained) NSTextView *logText;

@end

@interface GetRemoteCrashDataManager : NSObject

/*
 {
 @"client":@"apple",
 @"clientVersion":@"5.5.0"
 @"build":@"125580",
 @"uuid":@"781240120912480128312",
 @"pin":@"673302055",
 @"partner":@"pp601",
 @"startTime":@"yyyy-MM-dd 00:00:00",
 @"endTime":@"yyyy-MM-dd 23:59:59",
 @"fileName":@"iPhone_550_PP3"
 }
 */
+(void)getOperationCookie:(NSDictionary*)paramDic andVC:(id<GetRemoteCrashDataManagerVCDelegate>)crashVC;
+(void)getOperationCookie:(NSDictionary*)paramDic withCompleteBlock:(void(^)(BOOL suc))completeBlock;
+(void)getOperationCookie:(NSDictionary*)paramDic andVC:(id<GetRemoteCrashDataManagerVCDelegate>)crashVC withCompleteBlock:(void(^)(BOOL suc))completeBlock;

@end
