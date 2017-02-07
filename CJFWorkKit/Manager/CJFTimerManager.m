//
//  CJFTimerManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFTimerManager.h"
#import "NSTimer+Weak.h"

//所有注册的事件在此处做一个备份
NSString* const TT_CrashTask    = @"TT_CrashTask";


@interface CJFTimerManager ()

@property(nonatomic,strong) NSTimer* updateTimer;
@property(nonatomic,strong) NSMutableDictionary<NSString*,executeBlock>* updateBlockList;

@end

@implementation CJFTimerManager

+(CJFTimerManager*)sharedManager
{
    static CJFTimerManager* _sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedManager = [[CJFTimerManager alloc] init];
    });
    return _sharedManager;
}

-(void)dealloc
{
    if( _updateTimer ){
        [_updateTimer invalidate];
        _updateTimer = nil;
    }
}

- (instancetype)init
{
    self = [super init];
    if (self) {
        __weak __typeof(self) weakSelf = self;
        _updateTimer = [NSTimer scheduledTimerWithTimeInterval:50.0f block:^{
            [weakSelf updateTimerHanlder];
        } repeats:YES andModel:NSRunLoopCommonModes];
        self.updateBlockList = [[NSMutableDictionary alloc] initWithCapacity:10];
    }
    return self;
}

-(void)updateTimerHanlder
{
    for( NSString* keyStr in self.updateBlockList.allKeys){
        executeBlock block = self.updateBlockList[keyStr];
        if( block ){
            block();
        }
    }
}

-(void)addExecuteBlock:(executeBlock)block andKey:(NSString*)keyName
{
    if( block == nil || !validateString(keyName)){
        return;
    }
    self.updateBlockList[keyName] = block;
}

-(void)removeExecuteBlockWithKey:(NSString*)keyName
{
    if( !validateString(keyName) ){
        return;
    }
    [self.updateBlockList removeObjectForKey:keyName];
}

@end
