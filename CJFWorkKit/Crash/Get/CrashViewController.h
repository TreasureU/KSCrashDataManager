//
//  CrashViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/6/22.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "GetRemoteCrashDataManager.h"

@interface CrashViewController : NSViewController <GetRemoteCrashDataManagerVCDelegate>

@property (weak) IBOutlet NSPopUpButton *clientChoiceBtn;
@property (weak) IBOutlet NSTextField *versionLab;
@property (weak) IBOutlet NSTextField *buildLab;
@property (weak) IBOutlet NSTextField *UUIDLab;
@property (weak) IBOutlet NSTextField *userNameLab;
@property (weak) IBOutlet NSTextField *pipeLab;
@property (weak) IBOutlet NSTextField *crashStartLab;
@property (weak) IBOutlet NSTextField *crashEndLab;
@property (weak) IBOutlet NSTextField *fileNameLab;

- (IBAction)confirmBtnClick:(NSButton *)sender;
- (IBAction)resetBtnClick:(NSButton *)sender;

@property (unsafe_unretained) IBOutlet NSTextView *logText;

@end
