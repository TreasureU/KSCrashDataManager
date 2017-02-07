//
//  CJFNetworkManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/5/4.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFNetworkManager.h"

@implementation CJFNetworkManager

+ (instancetype)sharedClient {
    static CJFNetworkManager *_sharedClient = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedClient = [[CJFNetworkManager alloc] initWithBaseURL:nil];
        _sharedClient.securityPolicy.allowInvalidCertificates = YES;
    });
    
    return _sharedClient;
}

+ (instancetype)newClient{
    CJFNetworkManager* manager = [[CJFNetworkManager alloc] initWithBaseURL:nil];
    manager.securityPolicy.allowInvalidCertificates = YES;
    return manager;
}

-(CJFNetworkManager*)setHttpHeader:(CJFNetworkType)type
{
    switch (type) {
        case CJFNetworkNone: {
            self.requestSerializer = [AFHTTPRequestSerializer serializer];
            self.responseSerializer = [AFHTTPResponseSerializer serializer];
            
            [self.requestSerializer setValue:CJF_USER_AGENT forHTTPHeaderField:@"User-Agent"];
            break;
        }
        case CJFNetworkCrashQuery:{
            self.requestSerializer = [AFHTTPRequestSerializer serializer];
            self.responseSerializer = [AFHTTPResponseSerializer serializer];
            [self.requestSerializer setValue:CJF_USER_AGENT forHTTPHeaderField:@"User-Agent"];
            [self.requestSerializer setValue:@"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" forHTTPHeaderField:@"Accept"];
            [self.requestSerializer setValue:@"1" forHTTPHeaderField:@"DNT"];
            [self.requestSerializer setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
            [self.requestSerializer setValue:@"http://ccadmin.m.jd.com/admin/exception/list.action" forHTTPHeaderField:@"Referer"];
            [self.requestSerializer setValue:@"gzip, deflate" forHTTPHeaderField:@"Accept-Encoding"];
            [self.requestSerializer setValue:@"en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2" forHTTPHeaderField:@"Accept-Language"];
            [self.requestSerializer setValue:@"max-age=0" forHTTPHeaderField:@"Cache-Control"];
            [self.requestSerializer setValue:@"http://ccadmin.m.jd.com" forHTTPHeaderField:@"Origin"];
            [self.requestSerializer setValue:@"1" forHTTPHeaderField:@"Upgrade-Insecure-Requests"];
            break;
        }
        case CJFNetworkCrashDetail:{
            self.requestSerializer = [AFHTTPRequestSerializer serializer];
            self.responseSerializer = [AFHTTPResponseSerializer serializer];
            [self.requestSerializer setValue:CJF_USER_AGENT forHTTPHeaderField:@"User-Agent"];
            [self.requestSerializer setValue:@"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" forHTTPHeaderField:@"Accept"];
            [self.requestSerializer setValue:@"1" forHTTPHeaderField:@"Upgrade-Insecure-Requests"];
            [self.requestSerializer setValue:@"1" forHTTPHeaderField:@"DNT"];
            [self.requestSerializer setValue:@"application/x-www-form-urlencoded; charset=UTF-8" forHTTPHeaderField:@"Content-Type"];
            [self.requestSerializer setValue:@"http://ccadmin.m.jd.com/admin/exception/list.action" forHTTPHeaderField:@"Referer"];
            [self.requestSerializer setValue:@"gzip, deflate, sdch" forHTTPHeaderField:@"Accept-Encoding"];
            [self.requestSerializer setValue:@"en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2" forHTTPHeaderField:@"Accept-Language"];
            break;
        }
        default:{
            self.requestSerializer = [AFHTTPRequestSerializer serializer];
            self.responseSerializer = [AFHTTPResponseSerializer serializer];
            [self.requestSerializer setValue:CJF_USER_AGENT forHTTPHeaderField:@"User-Agent"];
        }
    }
    return self;
}

+(void)clearAllCookies
{
    NSArray *cookiesArray = [[NSHTTPCookieStorage sharedHTTPCookieStorage] cookies];
    for (NSHTTPCookie *cookie in cookiesArray) {
        [[NSHTTPCookieStorage sharedHTTPCookieStorage] deleteCookie:cookie];
    }
}

@end
