//
//  CJFWindowController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>


@interface CJFWindowController : NSWindowController

@property(nonatomic,strong) NSString* functionName;

+(CJFWindowController*)showNewWindowWithControllerName:(NSString*)name;

@end
