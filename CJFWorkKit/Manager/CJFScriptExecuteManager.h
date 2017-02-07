//
//  CJFScriptExecuteManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/23.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, CJFScriptType) {
    //单独脚本
    CJFScriptNone,
    CJFScriptParser,
    CJFScriptClassifyInit,
    CJFScriptClassifyRecursion,
    CJFScriptClassifyFinal,
    CJFScriptOOMClassify,
    CJFScriptQuicklyCount,
    CJFScriptExcel,
    CJFScriptNAV_URL,
    
    //组合脚本
    CJFScriptClassifyGroup, //init->recursion->final
    CJFScriptNormalCrashParserGroup,    //paeser->init->recursion->final
};

@interface CJFScriptExecuteManager : NSObject

+(CJFScriptExecuteManager*)sharedManager;

//可执行函数
-(NSString*)syncExcuteScript:(CJFScriptType)scriptName andParamDic:(NSDictionary*)paramDic;
-(BOOL)asyncExcuteScript:(CJFScriptType)scriptName andParamDic:(NSDictionary*)paramDic withCompleteBlock:(void (^)(NSString* result))completeBlock;

@end
