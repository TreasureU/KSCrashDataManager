//
//  TimedTaskController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "TimedTaskController.h"
#import "CrashTaskDataManager.h"

@interface TimedTaskController ()

@end

@implementation TimedTaskController

- (instancetype)init
{
    self = [super init];
    if (self) {
        _editModel = nil;
    }
    return self;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    if( self.editModel ){
        [self.clientChoiceBtn selectItemWithTitle:self.editModel.clientChoiceBtn];
        self.versionLab.stringValue = self.editModel .versionLab;
        self.buildLab.stringValue = self.editModel .buildLab;
        self.UUIDLab.stringValue = self.editModel .UUIDLab;
        self.userNameLab.stringValue = self.editModel .userNameLab;
        self.pipeLab.stringValue = self.editModel .pipeLab;
        self.fileNameLab.stringValue = self.editModel .fileNameLab;
        self.dirNameLab.stringValue = self.editModel .dirNameLab;
        BOOL allState = YES;
        for( int i = 1; i < 8; i ++ ){
            NSInteger weekState = ( [self.editModel getValidateCrashWeekByIndex:i] ? 1 : 0 );
            NSInteger scriptState = ( [self.editModel getValidateCTMScriptByIndex:i] ? 1 : 0 );
            if( !weekState ){
                allState = NO;
            }
            [self weekBtnWithTag:i].state = weekState;
            [self scriptBtnWithTag:i].state = scriptState;
        }
        self.allWeekBtn.state = ( allState ? 1 : 0 );
    }else{
        [self resetUIShow];
    }
}

#pragma mark - confirm && reset btn

- (IBAction)confirmBtnClick:(NSButton *)sender {
    CrashTimedModel* model = self.editModel;
    if( model != nil ){
        if( self.editModel.taskState == CTTState_Going ){
            NSLog(@"当前模型正在执行中，不允许修改");
            [self addTextLogWithString:@"当前模型正在执行中，不允许修改"];
            return;
        }
    }else{
        model = [[CrashTimedModel alloc] init];
    }
    model.clientChoiceBtn = self.clientChoiceBtn.selectedItem.title;
    model.versionLab = self.versionLab.stringValue;
    model.buildLab = self.buildLab.stringValue;
    model.UUIDLab = self.UUIDLab.stringValue;
    model.userNameLab = self.userNameLab.stringValue;
    model.pipeLab = self.pipeLab.stringValue;
    model.fileNameLab = self.fileNameLab.stringValue;
    model.dirNameLab = self.dirNameLab.stringValue;
    
    model.validateWeek = PMValidateNone;
    model.validateScript = CTMScript_None;
    for (int i = 1; i < 8; i ++) {
        NSButton* weekbtn = [self weekBtnWithTag:i];
        NSButton* scriptBtn = [self scriptBtnWithTag:i];
        if( weekbtn.state ){
            [model addValidateCrashWeekByIndex:i];
        }
        if( scriptBtn.state ){
            [model addValidateCTMScriptByIndex:i];
        }
    }
    if( self.editModel == nil ){
        NSLog(@"模型添加成功");
        [self addTextLogWithString:@"模型添加成功"];
        [[CrashTaskDataManager sharedManager] addCrashModel:model];
    }else{
        NSLog(@"模型修改成功");
        [self addTextLogWithString:@"模型修改成功"];
    }
}

- (IBAction)resetBtnClick:(NSButton *)sender {
    [self resetUIShow];
}

-(void)resetUIShow{
    [self.clientChoiceBtn selectItemWithTitle:@"iPad"];
    self.versionLab.stringValue = @"";
    self.buildLab.stringValue = @"";
    self.UUIDLab.stringValue = @"";
    self.userNameLab.stringValue = @"";
    self.pipeLab.stringValue = @"";
    self.fileNameLab.stringValue = @"";
    self.dirNameLab.stringValue = @"";
    
    for (int index = 0; index < 8; index++) {
        [self scriptBtnWithTag:index].state = 1;
        [self weekBtnWithTag:index].state = 1;
    }
    
    self.logText.string = @"--------------------- log -------------------\n";
}

-(void)addTextLogWithString:(NSString*)str
{
    self.logText.string = [self.logText.string stringByAppendingString:[NSString stringWithFormat:@"%@\n",str]];
}

#pragma mark - script btn selected
- (IBAction)selectScriptBtnClick:(NSButton *)sender {
    NSInteger state = sender.state;
    NSInteger startTag = 0;
    NSInteger endTag = 0;
    
    switch (sender.tag) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
            if( state ){
                startTag = 1;
                endTag = sender.tag - 1;
            }else{
                startTag = sender.tag + 1;
                endTag = 5;
            }
            if( startTag <= 5 && endTag >= 1 ){
                for(; startTag <= endTag; startTag ++  ){
                    [self scriptBtnWithTag:startTag].state = state;
                }
            }
            break;
        case 6:
            if( state ){
                self.translateBtn.state = state;
                self.parserBtn.state = state;
            }
            break;
        default:
            break;
    }
}

-(NSButton*)scriptBtnWithTag:(NSInteger)tag
{
    switch (tag) {
        case 1:
            return self.translateBtn;
            break;
        case 2:
            return self.parserBtn;
            break;
        case 3:
            return self.classifyInitBtn;
            break;
        case 4:
            return self.classifyRecuBtn;
            break;
        case 5:
            return self.classifyFinalBtn;
            break;
        case 6:
            return self.OOMBtn;
            break;
        default:
            return nil;
            break;
    }
}

#pragma mark - week btn selected
- (IBAction)selectWeekBtnClick:(NSButton *)sender {
    NSInteger state = sender.state;
    
    if( sender == self.allWeekBtn ){
        for( int i = 1; i < 8 ; i ++ ){
            [self weekBtnWithTag:i].state = state;
        }
    }else{
        if( !state ){
            self.allWeekBtn.state = 0;
        }
    }
}

-(NSButton*)weekBtnWithTag:(NSInteger)tag
{
    switch (tag) {
        case 1:
            return self.monBtn;
            break;
        case 2:
            return self.tueBtn;
            break;
        case 3:
            return self.wedBtn;
            break;
        case 4:
            return self.thuBtn;
            break;
        case 5:
            return self.friBtn;
            break;
        case 6:
            return self.satBtn;
            break;
        case 7:
            return self.sunBtn;
            break;
        case 8:
            return self.allWeekBtn;
            break;
        default:
            return nil;
            break;
    }
}

@end
