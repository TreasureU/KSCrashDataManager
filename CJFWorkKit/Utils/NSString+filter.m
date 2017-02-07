//
//  NSString+filter.m
//  CheckInApp
//
//  Created by ChengJianFeng on 16/3/11.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "NSString+filter.h"

@implementation NSString(filter)

- (NSString *)filterStartWith:(NSString *)start endWith:(NSString *)end
{
    //NSRegularExpression类里面调用表达的方法需要传递一个NSError的参数。下面定义一个
    NSError *error;
    //http+:[^\\s]* 这个表达式是检测一个网址的。(?<=title\>).*(?=</title)截取html文章中的<title></title>中内文字的正则表达式
    NSString *filter = [NSString stringWithFormat: @"(?%@).*(?=%@)", start, end];
    NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:filter
                                                                           options:0
                                                                             error:&error];
    if (regex != nil)
    {
        NSTextCheckingResult *firstMatch=[regex firstMatchInString:self options:0 range:NSMakeRange(0, [self length])];
        if (firstMatch)
        {
            NSRange resultRange = [firstMatch rangeAtIndex:0];
            
            //从urlString当中截取数据
            NSString *result=[self substringWithRange:resultRange];
            //输出结果
            return result;
        }
    }
    
    return nil;
}

- (NSArray *)componentsSeparatedFromString:(NSString *)fromString toString:(NSString *)toString
{
    if ( !validateString(self) || !validateString(fromString) || !validateString(toString)) {
        return nil;
    }
    NSMutableArray *subStringsArray = [[NSMutableArray alloc] init];
    NSString *tempString = self;
    NSRange range = [tempString rangeOfString:fromString];
    while (range.location != NSNotFound) {
        tempString = [tempString substringFromIndex:(range.location + range.length)];
        range = [tempString rangeOfString:toString];
        if (range.location != NSNotFound) {
            [subStringsArray addObject:[tempString substringToIndex:range.location]];
            range = [tempString rangeOfString:fromString];
        }
        else
        {
            break;
        }
    }
    return subStringsArray;
}

- (NSInteger)findString:(NSString*)subStr withCount:(NSInteger)count
{
    if( !validateString(subStr) || !validateString(self) || count <= 0 ){
        return NSNotFound;
    }
    NSString* myStr = self;
    NSInteger location = NSNotFound;
    for( int i = 0; i < count; i ++ ){
        NSRange range = [myStr rangeOfString:subStr];
        if( range.location == NSNotFound ){
            break;
        }else{
            if( location == NSNotFound ){
                location = range.location;
            }else{
                location = location + subStr.length + range.location;
            }
            myStr = [myStr substringFromIndex:range.location + subStr.length];
        }
    }
    return location;
}

- (NSString *)SplitStringToEnd:(NSString*)subStr withCount:(NSInteger)count
{
    NSInteger location = [self findString:subStr withCount:count];
    if( location != NSNotFound ){
        return [self substringFromIndex:(location + subStr.length)];
    }else{
        return nil;
    }
}

+ (NSString *)stringWithUUID {
    CFUUIDRef uuid = CFUUIDCreate(NULL);
    CFStringRef string = CFUUIDCreateString(NULL, uuid);
    CFRelease(uuid);
    return (__bridge_transfer NSString *)string;
}

+ (NSString*)randomLengthString:(NSInteger)length
{
    if(length <= 0){
        return @"";
    }
    char data[length];
    for (int x=0;x<length;data[x++] = (char)('A' + (arc4random_uniform(26))));
    return [[NSString alloc] initWithBytes:data length:length encoding:NSUTF8StringEncoding];
}

+ (NSString*)randomnNumberStringWithLength:(NSInteger)length
{
    if(length <= 0){
        return @"";
    }
    char data[length];
    for ( int index=0 ; index <length; index ++){
        int random = arc4random_uniform(9);
        data[index] = (char)('0' + random);
    }
    return [[NSString alloc] initWithBytes:data length:length encoding:NSUTF8StringEncoding];
}

-(NSInteger)subStringCount:(NSString*)subStr
{
    if( !validateString(subStr) || !validateString(self) ){
        return 0;
    }
    
    NSInteger index = 0;
    NSInteger count = 0;
    while (index + subStr.length <= self.length ) {
        NSString* sub = [self substringWithRange:NSMakeRange(index, subStr.length)];
        if( [subStr isEqualToString:sub] ){
            count++;
        }
        index += subStr.length;
    }
    return count;
}

@end
