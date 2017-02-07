//
//  NSTimer+Weak.m
//  shizhen
//
//  Created by hunter on 16/4/18.
//  Copyright © 2016年 hunter. All rights reserved.
//

#import "NSTimer+Weak.h"

@implementation NSTimer(Weak)

+(NSTimer*)scheduledTimerWithTimeInterval:(NSTimeInterval)interval block:(void(^)())block repeats:(BOOL)repeats
{
    return [self scheduledTimerWithTimeInterval:interval target:self selector:@selector(timerUpdateWithBlock:) userInfo:[block copy] repeats:repeats];
}

+(NSTimer*)scheduledTimerWithTimeInterval:(NSTimeInterval)interval block:(void(^)())block repeats:(BOOL)repeats andModel:(NSString*)model
{
    if( !model || ( ![model isEqualToString:NSRunLoopCommonModes] && [model isEqualToString:NSDefaultRunLoopMode]) ){
        model = NSDefaultRunLoopMode;
    }
    NSTimer* timer = [NSTimer timerWithTimeInterval:interval target:self selector:@selector(timerUpdateWithBlock:) userInfo:[block copy]  repeats:repeats];
    [[NSRunLoop mainRunLoop] addTimer:timer forMode:model];
    return timer;
}


+(void)timerUpdateWithBlock:(NSTimer*)timer{
    void (^myBlock)() = timer.userInfo;
    if( myBlock ){
        myBlock();
    }
}

@end
