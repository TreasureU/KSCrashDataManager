//
//  CrashTimedModel.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef NS_OPTIONS(NSUInteger, PMValidateWeek) {
    PMValidateNone = 0,
    PMValidateMon = 1 << 0,
    PMValidateTue = 1 << 1,
    PMValidateWed = 1 << 2,
    PMValidateThu = 1 << 3,
    PMValidateFri = 1 << 4,
    PMValidateSat = 1 << 5,
    PMValidateSun = 1 << 6,
};

typedef NS_ENUM(NSUInteger, CTTState) {
    CTTState_None,
    CTTState_Going,
    CTTState_Finish,
    CTTState_Failed,
};

typedef NS_OPTIONS(NSUInteger,CTMScript ) {
    CTMScript_None = 0,
    CTMScript_translate = 1 << 0,
    CTMScript_parser = 1 << 1,
    CTMScript_classifyInit = 1 << 2,
    CTMScript_classifyRecu = 1 << 3,
    CTMScript_classifyFinal = 1 << 4,
    CTMScript_OOM = 1 << 5,
};

@interface CrashTimedModel : NSObject

@property(assign) CTTState taskState;

@property (copy) NSString *clientChoiceBtn;
@property (copy) NSString *versionLab;
@property (copy) NSString *buildLab;
@property (copy) NSString *UUIDLab;
@property (copy) NSString *userNameLab;
@property (copy) NSString *pipeLab;
@property (copy) NSString *fileNameLab;
@property (copy) NSString *dirNameLab;

@property(assign) PMValidateWeek validateWeek;
@property(assign) CTMScript validateScript;

-(void)addValidateCrashWeekByIndex:(NSInteger)index;
-(BOOL)getValidateCrashWeek:(NSString*)name;
-(BOOL)getValidateCrashWeekByIndex:(NSInteger)index;
+(PMValidateWeek)getPMValidateWeekByIndex:(NSInteger)index;
+(PMValidateWeek)getPMValidateWeekByString:(NSString*)name;

-(void)addValidateCTMScriptByIndex:(NSInteger)index;
-(BOOL)getValidateCTMScriptByIndex:(NSInteger)index;
+(CTMScript)getCTMScriptByIndex:(NSInteger)index;

-(NSString*)getValueByIdentifier:(NSString*)identifier;

@end
