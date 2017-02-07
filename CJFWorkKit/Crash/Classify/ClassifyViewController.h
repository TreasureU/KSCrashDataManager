//
//  ClassifyViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface ClassifyViewController : NSViewController

@property (weak) IBOutlet NSPopUpButton *appNameBtn;
@property (weak) IBOutlet NSPopUpButton *fileSelectedBtn;
@property (weak) IBOutlet NSPopUpButton *compareSelectedBtn;


@property (unsafe_unretained) IBOutlet NSTextView *logText;
@property (weak) IBOutlet NSPopUpButton *scriptBtn;

- (IBAction)runBtnClick:(NSButton *)sender;

@end
