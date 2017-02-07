//
//  NSData+Sperate.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/8/29.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "NSData+Sperate.h"

@implementation NSData(Sperate)

- (void)obj_enumerateComponentsSeparatedBy:(NSData *)delimiter usingBlock:(EnumerateBlock)block
{
    //current location in data
    NSUInteger location = 0;
    
    while (YES) {
        //get a new component separated by delimiter
        NSRange rangeOfDelimiter = [self rangeOfData:delimiter
                                             options:0
                                               range:NSMakeRange(location, self.length - location)];
        
        //has reached the last component
        if (rangeOfDelimiter.location == NSNotFound) {
            break;
        }
        
        NSRange rangeOfNewComponent = NSMakeRange(location, rangeOfDelimiter.location - location + delimiter.length);
        //get the data of every component
        NSData *everyComponent = [self subdataWithRange:rangeOfNewComponent];
        //invoke the block
        if( block ){
            block(everyComponent, NO);
        }
        //make the offset of location
        location = NSMaxRange(rangeOfNewComponent);
    }
    
    //reminding data
    NSData *reminder = [self subdataWithRange:NSMakeRange(location, self.length - location)];
    //handle reminding data
    if( block ){
        block(reminder, YES);
    }
}

@end
