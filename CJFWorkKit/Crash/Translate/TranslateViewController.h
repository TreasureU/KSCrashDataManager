//
//  TranslateViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface TranslateViewController : NSViewController

@property (weak) IBOutlet NSPopUpButton *appNameBtn;
@property (weak) IBOutlet NSPopUpButton *fileSelectedBtn;
@property (weak) IBOutlet NSPopUpButton *OOMSelectedBtn;


@property (unsafe_unretained) IBOutlet NSTextView *logText;

- (IBAction)runBtnClick:(NSButton *)sender;

@end
