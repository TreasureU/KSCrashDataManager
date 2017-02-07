//
//  CrashTaskManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CrashTaskManager.h"
#import "CJFTimerManager.h"
#import "CrashTaskDataManager.h"

@implementation CrashTaskManager

- (instancetype)init
{
    self = [super init];
    if (self) {
        __weak __typeof(self) weakSelf = self;
        [[CJFTimerManager sharedManager] addExecuteBlock:^{
            [weakSelf updateTimerHanlder];
        } andKey:TT_CrashTask];
    }
    return self;
}

+(CrashTaskManager*)shareManager
{
    static CrashTaskManager* _sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        [CrashTaskDataManager sharedManager];
        _sharedManager = [[CrashTaskManager alloc] init];
    });
    return _sharedManager;
}

-(void)updateTimerHanlder
{
    //降低订餐调用频率
    static BOOL isNeedTask = YES;
    
    //一点钟时模型时间随机化
    NSString* nowDate = [[NSDate date] hours_minutes];
    NSString* nowWeek = [[NSDate date] weekName];
    
    //一点钟时做特殊的事情
    if( [nowDate isEqualToString:@"01:00"] ){
        isNeedTask = YES;
        for ( CrashTimedModel* model  in [CrashTaskDataManager sharedManager].crashArr ) {
            model.taskState = CTTState_None;
        }
        return;
    }
    
    if( isNeedTask && ([nowDate isEqualToString:@"04:00"] || [nowDate isEqualToString:@"05:00"] || [nowDate isEqualToString:@"06:00"]) ){
        isNeedTask = NO;
        NSLog(@"\n\n\n------------------开始crash定时任务----------------\n");
        //模型时间校验
        for ( CrashTimedModel* model  in [CrashTaskDataManager sharedManager].crashArr ) {
            if( [model getValidateCrashWeek:nowWeek] && model.taskState == CTTState_None ){
                //执行定时任务
                
            }
        }
        NSLog(@"\n------------------开始crash定时任务----------------\n\n\n");
    }
    return;
}


@end
