//
//  TimedTaskController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "CrashTimedModel.h"

@interface TimedTaskController : NSViewController

@property (weak) IBOutlet NSPopUpButton *clientChoiceBtn;
@property (weak) IBOutlet NSTextField *versionLab;
@property (weak) IBOutlet NSTextField *buildLab;
@property (weak) IBOutlet NSTextField *UUIDLab;
@property (weak) IBOutlet NSTextField *userNameLab;
@property (weak) IBOutlet NSTextField *pipeLab;
@property (weak) IBOutlet NSTextField *fileNameLab;
@property (weak) IBOutlet NSTextField *dirNameLab;

@property (weak) IBOutlet NSButton *monBtn;
@property (weak) IBOutlet NSButton *tueBtn;
@property (weak) IBOutlet NSButton *wedBtn;
@property (weak) IBOutlet NSButton *thuBtn;
@property (weak) IBOutlet NSButton *friBtn;
@property (weak) IBOutlet NSButton *satBtn;
@property (weak) IBOutlet NSButton *sunBtn;
@property (weak) IBOutlet NSButton *allWeekBtn;

@property (weak) IBOutlet NSButton *translateBtn;
@property (weak) IBOutlet NSButton *parserBtn;
@property (weak) IBOutlet NSButton *OOMBtn;
@property (weak) IBOutlet NSButton *classifyInitBtn;
@property (weak) IBOutlet NSButton *classifyRecuBtn;
@property (weak) IBOutlet NSButton *classifyFinalBtn;

@property (unsafe_unretained) IBOutlet NSTextView *logText;

@property (strong) CrashTimedModel* editModel;

@end
