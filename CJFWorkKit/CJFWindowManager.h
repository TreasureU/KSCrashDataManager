//
//  CJFWindowManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>


extern NSString* const  FN_LocalConvert;         //本地提取
extern NSString* const  FN_Parser;               //解析
extern NSString* const  FN_Classify;             //归类
extern NSString* const  FN_OOM;                  //OOM归类

extern NSString* const  FN_QuickCount;          //快速统计
extern NSString* const  FN_Excel;               //Excel
extern NSString* const  FN_NavUrl;              //Nav Url统计

extern NSString* const FN_NetworkGet;           //网络拉取
extern NSString* const  FN_TimedTask;            //定时任务

extern NSString* const FN_LocalCrash_ShortCut;  //本地解析快捷方式
extern NSString* const FN_QuicklyImport;    //快捷文件导入方式

@interface CJFWindowManager : NSObject

+(CJFWindowManager*)sharedManager;
-(void)presentNewWindowWithName:(NSString*)VCName;
-(void)closeWindowWithNotifaction:(NSString*)VCName;

@end
