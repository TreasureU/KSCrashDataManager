//
//  CJFTimerManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

extern NSString* const TT_CrashTask;

typedef void(^executeBlock)();

@interface CJFTimerManager : NSObject

+(CJFTimerManager*)sharedManager;

-(void)addExecuteBlock:(executeBlock)block andKey:(NSString*)keyName;
-(void)removeExecuteBlockWithKey:(NSString*)keyName;

@end
