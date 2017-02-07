//
//  NSTimer+Weak.h
//  shizhen
//
//  Created by hunter on 16/4/18.
//  Copyright © 2016年 hunter. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface NSTimer(Weak)

+(NSTimer*)scheduledTimerWithTimeInterval:(NSTimeInterval)interval block:(void(^)())block repeats:(BOOL)repeats;

+(NSTimer*)scheduledTimerWithTimeInterval:(NSTimeInterval)interval block:(void(^)())block repeats:(BOOL)repeats andModel:(NSString*)model;

@end
