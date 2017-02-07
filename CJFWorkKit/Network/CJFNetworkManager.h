//
//  CJFNetworkManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/5/4.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

@interface CJFNetworkManager : AFHTTPSessionManager

typedef NS_ENUM(NSUInteger, CJFNetworkType) {
    CJFNetworkNone,
    
    CJFNetworkCrashQuery,
    CJFNetworkCrashDetail
};

+ (instancetype)sharedClient;

+ (instancetype)newClient;

-(CJFNetworkManager*)setHttpHeader:(CJFNetworkType)type;

+(void)clearAllCookies;

@end
