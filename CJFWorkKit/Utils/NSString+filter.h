//
//  NSString+filter.h
//  CheckInApp
//
//  Created by ChengJianFeng on 16/3/11.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSString(filter)
- (NSString *)filterStartWith:(NSString *)start endWith:(NSString *)end;
- (NSArray *)componentsSeparatedFromString:(NSString *)fromString toString:(NSString *)toString;
- (NSInteger)findString:(NSString*)subStr withCount:(NSInteger)count;
- (NSString *)SplitStringToEnd:(NSString*)subStr withCount:(NSInteger)count;
+ (NSString *)stringWithUUID;
+ (NSString*)randomLengthString:(NSInteger)length;
+ (NSString*)randomnNumberStringWithLength:(NSInteger)length;
-(NSInteger)subStringCount:(NSString*)subStr;
@end
