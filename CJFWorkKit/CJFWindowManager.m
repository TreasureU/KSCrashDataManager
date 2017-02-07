//
//  CJFWindowManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFWindowManager.h"
#import "CJFWindowController.h"


NSString* const FN_LocalConvert = @"StatisticsVC";   //本地提取
NSString* const FN_Parser = @"ParserVC";             //解析
NSString* const FN_Classify = @"ClassifyVC";         //归类
NSString* const FN_OOM = @"TranslateVC";             //OOM归类

NSString* const FN_QuickCount = @"QuickCountVC";     //快速统计
NSString* const FN_Excel = @"ExcelVC";               //Excel
NSString* const FN_NavUrl = @"NavUrlCountVC";        //Nav Url统计

NSString* const FN_NetworkGet = @"CrashVC";          //网络拉取
NSString* const FN_TimedTask = @"TimedTaskTableVC";  //定时任务

NSString* const FN_LocalCrash_ShortCut = @"LocalCrashShortcutVC";   //本地解析快捷方式
NSString* const FN_QuicklyImport = @"QuicklyImportVC";   //快捷导入文件

@interface CJFWindowManager ()

@property(atomic,strong) NSMutableDictionary<NSString*,CJFWindowController*> *subWindowList;

@end

@implementation CJFWindowManager

- (instancetype)init
{
    self = [super init];
    if (self) {
        self.subWindowList = [[NSMutableDictionary alloc] initWithCapacity:10];
    }
    return self;
}

+(CJFWindowManager*)sharedManager
{
    static CJFWindowManager* _sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedManager = [[CJFWindowManager alloc] init];
    });
    return _sharedManager;
}

-(void)presentNewWindowWithName:(NSString*)VCName
{
    if ( !validateString(VCName) ) {
        return;
    }
    if( self.subWindowList[VCName] != nil ){
        NSWindowController* oldWinVC = self.subWindowList[VCName];
        [oldWinVC.window setAnimationBehavior:NSWindowAnimationBehaviorAlertPanel];
        [oldWinVC.window orderFront:nil];
    }else{
        CJFWindowController* winVC = [CJFWindowController showNewWindowWithControllerName:VCName];
        if( winVC ){
            self.subWindowList[VCName] = winVC;
            [winVC.window setAnimationBehavior:NSWindowAnimationBehaviorAlertPanel];
            [winVC showWindow:self];
        }
    }
}

-(void)closeWindowWithNotifaction:(NSString*)VCName
{
    if( !validateString(VCName) ){
        return;
    }
    [self.subWindowList removeObjectForKey:VCName];
}

@end
