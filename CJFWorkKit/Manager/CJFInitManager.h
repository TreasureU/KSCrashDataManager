//
//  CJFInitManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/22.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>


@interface CJFInitManager : NSObject

+(CJFInitManager*)sharedManager;

-(void)InitEnvironment;
//强制重建所有脚本
-(void)forceScriptFileReplace;
//强制重建整个环境文件夹
-(void)rebuildEnvironment;

@end
