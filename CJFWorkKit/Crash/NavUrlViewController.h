//
//  NavUrlViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface NavUrlViewController : NSViewController

@property (weak) IBOutlet NSPopUpButton *appNameBtn;
@property (weak) IBOutlet NSPopUpButton *fileSelectedBtn;
@property (unsafe_unretained) IBOutlet NSTextView *logText;
@property (weak) IBOutlet NSTextField *sourceDirPath;
@property (weak) IBOutlet NSTextField *targetDirPath;

- (IBAction)runBtnClick:(NSButton *)sender;

@end
