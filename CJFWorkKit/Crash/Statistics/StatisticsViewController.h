//
//  StatisticsViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface StatisticsViewController : NSViewController

@property (weak) IBOutlet NSPopUpButton *fileSelectedBtn;
@property (weak) IBOutlet NSTextField *appendNameTF;
@property (weak) IBOutlet NSTextField *logText;


@property (weak) IBOutlet NSPopUpButton *appNameBtn;


- (IBAction)runBtnClick:(NSButton *)sender;

@end
