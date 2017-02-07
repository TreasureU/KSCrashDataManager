//
//  TimedTaskTableViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "TimedTaskTableViewController.h"
#import "CrashTaskDataManager.h"
#import "TimedTaskController.h"


@interface TimedTaskTableViewController ()<NSTableViewDelegate,NSTableViewDataSource>

@end

@implementation TimedTaskTableViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    self.tableView.delegate = self;
    self.tableView.dataSource = self;
    
}

#pragma mark - tableView delegate && datasource

- (NSInteger)numberOfRowsInTableView:(NSTableView *)tableView
{
    return [CrashTaskDataManager sharedManager].crashArr.count;
}

- (nullable id)tableView:(NSTableView *)tableView objectValueForTableColumn:(nullable NSTableColumn *)tableColumn row:(NSInteger)row
{
    return nil;
}

- (void)tableView:(NSTableView *)tableView setObjectValue:(nullable id)object forTableColumn:(nullable NSTableColumn *)tableColumn row:(NSInteger)row
{
    
}

- (nullable NSView *)tableView:(NSTableView *)tableView viewForTableColumn:(nullable NSTableColumn *)tableColumn row:(NSInteger)row
{
    NSView* cell = [[NSView alloc] init];
    NSTextField* text = [[NSTextField alloc] init];
    text.editable = NO;
    text.selectable = NO;
    if( row % 2 ){
        text.backgroundColor = [NSColor cyanColor];
    }else{
        text.backgroundColor = [NSColor colorWithRed:0.137f green:0.655f blue:1.0f alpha:1.0f];
    }
    text.alignment = NSTextAlignmentCenter;
    [cell addSubview:text];
    [text mas_makeConstraints:^(MASConstraintMaker *make) {
        make.edges.mas_equalTo(cell);
    }];
    text.stringValue = [(CrashTimedModel*)([CrashTaskDataManager sharedManager].crashArr[row]) getValueByIdentifier:tableColumn.identifier];
    return cell;
}

- (CGFloat)tableView:(NSTableView *)tableView heightOfRow:(NSInteger)row
{
    return 25.0f;
}

#pragma mark - button click

- (IBAction)addBtnClick:(NSButton *)sender {
    [self addTextLogWithString:@"add model operation!"];
    //跳转到下一个界面
    NSStoryboard* storyboard = [NSStoryboard storyboardWithName:@"Main" bundle:[NSBundle mainBundle]];
    [self presentViewControllerAsModalWindow:[storyboard instantiateControllerWithIdentifier:@"TimedTaskVC"]];
}

- (IBAction)refreshBtnClick:(NSButton *)sender {
    [self addTextLogWithString:@"refresh UI operation!"];
    [self.tableView reloadData];
}

- (IBAction)editBtnClick:(NSButton *)sender {
    NSInteger index = [self.tableView selectedRow];
    if( index < 0 ){
        [self addTextLogWithString:@"edit model operation failure!"];
        return;
    }
    
    CrashTimedModel* model = [CrashTaskDataManager sharedManager].crashArr[index];
    if( model.taskState == CTTState_Going ){
        [self addTextLogWithString:@"edit model operation falied: 模型正在执行 !"];
    }
    
    [self addTextLogWithString:@"edit model operation success!"];
    //跳转到下一个界面
    NSStoryboard* storyboard = [NSStoryboard storyboardWithName:@"Main" bundle:[NSBundle mainBundle]];
    TimedTaskController *vc = [storyboard instantiateControllerWithIdentifier:@"TimedTaskVC"];
    vc.editModel = model;
    
    NSLog(@"\n\n------------------编辑模型------------------\n%@\n-------------------------------\n\n",vc.editModel);
    
    [self presentViewControllerAsModalWindow:vc];
    
}

- (IBAction)removeBtnCilck:(NSButton *)sender {
    NSInteger index = [self.tableView selectedRow];
    if( index < 0 ){
        [self addTextLogWithString:@"remove model operation failure!"];
        return;
    }
    [self addTextLogWithString:@"remove model operation success!"];
    CrashTimedModel* model = [CrashTaskDataManager sharedManager].crashArr[index];
    NSLog(@"\n\n------------------删除模型------------------\n%@\n-------------------------------\n\n",model);
    [[CrashTaskDataManager sharedManager] deleteCrashModelByName:model.fileNameLab];
}

-(void)addTextLogWithString:(NSString*)str
{
    self.textView.string = [self.textView.string stringByAppendingString:[NSString stringWithFormat:@"%@ %@\n",[[NSDate date] year_month_day_hours_minutes],str]];
}

@end
