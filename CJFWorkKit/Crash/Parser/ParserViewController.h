//
//  ParserViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface ParserViewController : NSViewController

@property (weak) IBOutlet NSTextField *versionTF;
@property (weak) IBOutlet NSTextField *buildTF;
@property (weak) IBOutlet NSPopUpButton *dsymSelectedBtn;

@property (weak) IBOutlet NSPopUpButton *appNameBtn;
@property (weak) IBOutlet NSPopUpButton *fileSelectedBtn;
@property (unsafe_unretained) IBOutlet NSTextView *logText;
- (IBAction)runBtnClick:(NSButton *)sender;
- (IBAction)deviceTypeBtnClick:(NSPopUpButton *)sender;

@property (weak) IBOutlet NSTextField *grayValueTF;
@property (weak) IBOutlet NSButton *advancedBtn;



@end
