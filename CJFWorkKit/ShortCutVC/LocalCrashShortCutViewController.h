//
//  LocalCrashShortCutViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface LocalCrashShortCutViewController : NSViewController

@property (weak) IBOutlet NSTextField *versionTF;
@property (weak) IBOutlet NSTextField *buildTF;
@property (weak) IBOutlet NSPopUpButton *dsymSelectedBtn;

@property (weak) IBOutlet NSPopUpButton *appNameBtn;
@property (weak) IBOutlet NSPopUpButton *fileSelectedBtn;
@property (weak) IBOutlet NSTextField *targetDirName;


@property (weak) IBOutlet NSTextField *grayValueTF;
@property (weak) IBOutlet NSButton *advancedBtn;

@property (weak) IBOutlet NSPopUpButton *compareSelectedBtn;

@property (unsafe_unretained) IBOutlet NSTextView *logText;

@property (weak) IBOutlet NSButton *firstClsBtn;
@property (weak) IBOutlet NSButton *reClsBtn;
@property (weak) IBOutlet NSButton *finalClsBtn;

- (IBAction)clsBtnClick:(NSButton *)sender;


- (IBAction)runBtnClick:(NSButton *)sender;
- (IBAction)deviceTypeBtnClick:(NSPopUpButton *)sender;
- (IBAction)fileSelectedBtnClick:(NSPopUpButton *)sender;
- (IBAction)openDirBtnClick:(NSButton *)sender;


@end
