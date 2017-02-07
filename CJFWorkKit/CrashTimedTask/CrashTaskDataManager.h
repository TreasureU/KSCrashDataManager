//
//  CrashTaskDataManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "CrashTimedModel.h"

@interface CrashTaskDataManager : NSObject

+(CrashTaskDataManager*)sharedManager;

@property(copy,readonly) NSArray<CrashTimedModel*> *crashArr;

-(BOOL)addCrashModel:(CrashTimedModel*)model;

-(BOOL)deleteCrashModelByName:(NSString*)fileName;

-(BOOL)checkFileName:(NSString*)fileName;

-(BOOL)removeAllData;

-(BOOL)saveData;

@end
