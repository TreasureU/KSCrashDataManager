//
//  NSDate+HAndM.m
//  CheckInApp
//
//  Created by ChengJianFeng on 16/3/14.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "NSDate+HAndM.h"

@implementation NSDate(HAndM)

- (NSString *)weekName
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"EEEE";
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)hours_minutes
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"HH:mm";
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)hours_minutes_seconds
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"HH:mm:ss";
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)year_month_day
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"yyyy:MM:dd";//可以只格式化成局部数据
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)year_month_day_hours_minutes
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"yyyy:MM:dd-HH:mm";//可以只格式化成局部数据
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)year_month_day_hours_minutes_seconds_msec
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"yyyy_MM_dd_HH_mm_ss_SSS";//可以只格式化成局部数据
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)month_day_hours_minutes_seconds
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"MM_dd_HH_mm_ss";//可以只格式化成局部数据
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

- (NSString *)hours_minutes_seconds_msec
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"HH_mm_ss_SSS";//可以只格式化成局部数据
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

+(NSDate*)CJFdateFormatWithString:(NSString*)formatStr
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];
        df.dateFormat = @"yyyy:MM:dd-HH:mm";
        df.locale = [[NSLocale alloc] initWithLocaleIdentifier:@"zh_CN"];
    });
    if( !validateString(formatStr) ){
        return [NSDate dateWithTimeIntervalSinceNow:0];
    }
    NSDate* date = [df dateFromString:formatStr];
    return date;
}

-(NSString *)getCrashDateStyleStirng
{
    static NSDateFormatter *df = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        df = [[NSDateFormatter alloc] init];
        df.timeZone = [NSTimeZone systemTimeZone];//系统所在时区
        df.dateFormat = @"yyyy-MM-dd 00:00:00";//可以只格式化成局部数据
    });
    NSString *systemTimeZoneStr =  [df stringFromDate:self];
    return systemTimeZoneStr;
}

@end
