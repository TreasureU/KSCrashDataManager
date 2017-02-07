//
//  TimedTaskTableViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface TimedTaskTableViewController : NSViewController

@property (weak) IBOutlet NSTableView *tableView;
@property (unsafe_unretained) IBOutlet NSTextView *textView;

- (IBAction)addBtnClick:(NSButton *)sender;
- (IBAction)refreshBtnClick:(NSButton *)sender;
- (IBAction)editBtnClick:(NSButton *)sender;
- (IBAction)removeBtnCilck:(NSButton *)sender;

@end
