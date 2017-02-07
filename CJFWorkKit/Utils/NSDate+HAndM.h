//
//  NSDate+HAndM.h
//  CheckInApp
//
//  Created by ChengJianFeng on 16/3/14.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSDate(HHAndMM)
- (NSString *)weekName;
- (NSString *)hours_minutes;
- (NSString *)hours_minutes_seconds;
- (NSString *)year_month_day;
- (NSString *)year_month_day_hours_minutes;
- (NSString *)hours_minutes_seconds_msec;
- (NSString *)year_month_day_hours_minutes_seconds_msec;
+ (NSDate *)CJFdateFormatWithString:(NSString*)formatStr;
- (NSString *)month_day_hours_minutes_seconds;
-(NSString *)getCrashDateStyleStirng;
@end
