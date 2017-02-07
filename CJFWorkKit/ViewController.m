//
//  ViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/4/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "ViewController.h"
#import "CJFNetworkManager.h"
#import "CJFWindowController.h"
#import "CJFWindowManager.h"

@interface ViewController()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.tipLabel.stringValue = @"欢迎使用！~";
    // Do any additional setup after loading the view.
}


-(void)presentNewWindowWithName:(NSString*)VCName
{
    [[CJFWindowManager sharedManager] presentNewWindowWithName:VCName];
}

- (void)setRepresentedObject:(id)representedObject {
    [super setRepresentedObject:representedObject];

    // Update the view, if already loaded.
}


#pragma mark - function button

- (IBAction)crashBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_NetworkGet];
}

- (IBAction)parserBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_Parser];
}


- (IBAction)classifyBtnClick:(id)sender {
    [self presentNewWindowWithName:FN_Classify];
}

- (IBAction)statisticsBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_LocalConvert];
}

- (IBAction)translateBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_OOM];
}

- (IBAction)timedTaskBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_TimedTask];
}

- (IBAction)quickCountBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_QuickCount];
}

- (IBAction)excelBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_Excel];
}

- (IBAction)navUrlBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_NavUrl];
}

- (IBAction)localCrashShortcutBtnClick:(NSButton *)sender {
    [self presentNewWindowWithName:FN_LocalCrash_ShortCut];
}




@end
