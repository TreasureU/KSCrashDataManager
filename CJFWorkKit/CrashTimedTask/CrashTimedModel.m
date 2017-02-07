//
//  CrashTimedModel.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CrashTimedModel.h"

@implementation CrashTimedModel

- (instancetype)init
{
    self = [super init];
    if (self) {
        _clientChoiceBtn = nil;
        _versionLab = nil;
        _buildLab = nil;
        _UUIDLab = nil;
        _userNameLab = nil;
        _pipeLab = nil;
        _fileNameLab = nil;
        _dirNameLab = nil;
        _taskState = CTTState_None;
        
        _validateWeek = PMValidateNone;
        _validateScript = CTMScript_None;
    }
    return self;
}

- (void)encodeWithCoder:(NSCoder *)aCoder
{
    [aCoder encodeObject:_clientChoiceBtn forKey:@"clientChoiceBtn"];
    [aCoder encodeObject:_versionLab forKey:@"versionLab"];
    [aCoder encodeObject:_buildLab forKey:@"buildLab"];
    [aCoder encodeObject:_UUIDLab forKey:@"UUIDLab"];
    [aCoder encodeObject:_userNameLab forKey:@"userNameLab"];
    [aCoder encodeObject:_pipeLab forKey:@"pipeLab"];
    [aCoder encodeObject:_fileNameLab forKey:@"fileNameLab"];
    [aCoder encodeObject:_dirNameLab forKey:@"dirNameLab"];
    
    [aCoder encodeInteger:_validateWeek forKey:@"validateWeek"];
    [aCoder encodeInteger:_validateScript forKey:@"validateScript"];
}

- (instancetype)initWithCoder:(NSCoder *)coder
{
    self = [super init];
    if (self) {
        _taskState = CTTState_None;
        
        _clientChoiceBtn = [coder decodeObjectForKey:@"clientChoiceBtn"];
        _versionLab = [coder decodeObjectForKey:@"versionLab"];
        _buildLab = [coder decodeObjectForKey:@"buildLab"];
        _UUIDLab = [coder decodeObjectForKey:@"UUIDLab"];
        _userNameLab = [coder decodeObjectForKey:@"userNameLab"];
        _pipeLab = [coder decodeObjectForKey:@"pipeLab"];
        _fileNameLab = [coder decodeObjectForKey:@"fileNameLab"];
        _dirNameLab = [coder decodeObjectForKey:@"dirNameLab"];
        
        _validateWeek = [coder decodeIntegerForKey:@"validateWeek"];
        _validateScript = [coder decodeIntegerForKey:@"validateScript"];
    }
    return self;
}

#pragma mark - 获取相关属性

-(NSString*)getValueByIdentifier:(NSString*)identifier
{
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Warc-performSelector-leaks"
    if( [self respondsToSelector:NSSelectorFromString(identifier)] ){
        return [self performSelector:NSSelectorFromString(identifier) withObject:nil];
    }
    return @"";
#pragma clang diagnostic pop
}

#pragma mark - week相关

-(void)addValidateCrashWeekByIndex:(NSInteger)index
{
    self.validateWeek |= [[self class] getPMValidateWeekByIndex:index];
}

-(BOOL)getValidateCrashWeek:(NSString*)name
{
    PMValidateWeek week = PMValidateNone;
    //英文系统输出待验证
    if( validateString(name) ){
        week = [[self class] getPMValidateWeekByString:name];
    }
    
    if( self.validateWeek & week ){
        return YES;
    }else{
        return NO;
    }
}

-(BOOL)getValidateCrashWeekByIndex:(NSInteger)index
{
    PMValidateWeek week = PMValidateNone;
    //英文系统输出待验证
    if( index >= 1 && index <= 7 ){
        week = [[self class] getPMValidateWeekByIndex:index];
    }
    
    if( self.validateWeek & week ){
        return YES;
    }else{
        return NO;
    }
}

+(PMValidateWeek)getPMValidateWeekByIndex:(NSInteger)index
{
    PMValidateWeek week = PMValidateNone;
    switch (index) {
        case 1:
            week = PMValidateMon;
            break;
        case 2:
            week = PMValidateTue;
            break;
        case 3:
            week = PMValidateWed;
            break;
        case 4:
            week = PMValidateThu;
            break;
        case 5:
            week = PMValidateFri;
            break;
        case 6:
            week = PMValidateSat;
            break;
        case 7:
            week = PMValidateSun;
            break;
    }
    return week;
}

+(PMValidateWeek)getPMValidateWeekByString:(NSString*)name
{
    //英文系统输出待验证
    if( validateString(name) ){
        if( [name isEqualToString:@"星期一"] || [name isEqualToString:@"周一"] || [name isEqualToString:@"Monday"] || [name isEqualToString:@"Mon"] ){
            return PMValidateMon;
        }else if( [name isEqualToString:@"星期二"] || [name isEqualToString:@"周二"] || [name isEqualToString:@"Tuesday"] || [name isEqualToString:@"Tue"] ){
            return PMValidateTue;
        }else if( [name isEqualToString:@"星期三"] || [name isEqualToString:@"周三"] || [name isEqualToString:@"Wednesday"] || [name isEqualToString:@"Wed"] ){
            return PMValidateWed;
        }else if( [name isEqualToString:@"星期四"] || [name isEqualToString:@"周四"] || [name isEqualToString:@"Thursday"] || [name isEqualToString:@"Thu"] ){
            return PMValidateThu;
        }else if( [name isEqualToString:@"星期五"] || [name isEqualToString:@"周五"] || [name isEqualToString:@"Friday"] || [name isEqualToString:@"Fri"] ){
            return PMValidateFri;
        }else if( [name isEqualToString:@"星期六"] || [name isEqualToString:@"周六"] || [name isEqualToString:@"Saturday"] || [name isEqualToString:@"Sat"] ){
            return PMValidateSat;
        }else if( [name isEqualToString:@"星期日"] || [name isEqualToString:@"周日"] || [name isEqualToString:@"Sunday"] || [name isEqualToString:@"Sun"] ){
            return PMValidateSun;
        }
    }
    return PMValidateNone;
}

#pragma mark - 脚本相关

-(void)addValidateCTMScriptByIndex:(NSInteger)index
{
    self.validateScript |= [[self class] getCTMScriptByIndex:index];
}

-(BOOL)getValidateCTMScriptByIndex:(NSInteger)index
{
    CTMScript script = CTMScript_None;
    //英文系统输出待验证
    if( index >= 1 && index <= 6 ){
        script = [[self class] getCTMScriptByIndex:index];
    }
    
    if( self.validateScript & script ){
        return YES;
    }else{
        return NO;
    }
}

+(CTMScript)getCTMScriptByIndex:(NSInteger)index
{
    CTMScript week = CTMScript_None;
    switch (index) {
        case 1:
            return CTMScript_translate;
            break;
        case 2:
            return CTMScript_parser;
            break;
        case 3:
            return CTMScript_classifyInit;
            break;
        case 4:
            return CTMScript_classifyRecu;
            break;
        case 5:
            return CTMScript_classifyFinal;
            break;
        case 6:
            return CTMScript_OOM;
            break;
    }
    return week;
}

#pragma mark - Log

-(NSString*)description
{
    return [NSString stringWithFormat:@"< clientChoiceBtn = %@, versionLab = %@, buildLab = %@, UUIDLab = %@,userNameLab = %@, pipeLab = %@, fileNameLab = %%@ , dirNameLab =%@, validateWeek = %@, validateScript = %ld, taskState = %ld ",self.clientChoiceBtn,self.versionLab,self.buildLab,self.UUIDLab,self.userNameLab,self.pipeLab,self.fileNameLab,self.dirNameLab,self.validateWeek,self.validateScript];
}

-(NSString*)debugDescription
{
    return [self debugDescription];
}

@end
