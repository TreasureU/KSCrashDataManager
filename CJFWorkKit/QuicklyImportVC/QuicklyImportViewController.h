//
//  QuicklyImportViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>


@interface QuicklyImportViewController : NSViewController<CJFWindowDragVCDelegate>

@property (weak) IBOutlet NSPopUpButton *appNameBtn;
@property (weak) IBOutlet NSTextField *appendDesTF;
@property (weak) IBOutlet NSTextField *versionTF;
@property (weak) IBOutlet NSTextField *buildTF;
@property (weak) IBOutlet NSTextField *tipLabel;

- (IBAction)deviceBtnClick:(NSPopUpButton *)sender;

- (IBAction)importBtnClick:(NSButton *)sender;
- (IBAction)resetBtnClick:(NSButton *)sender;



@end
