//
//  CrashAccountViewController.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/12/6.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface CrashAccountViewController : NSViewController

@property (weak) IBOutlet NSTextField *accountTextFiled;
@property (weak) IBOutlet NSSecureTextField *passwordTextField;
@property (unsafe_unretained) IBOutlet NSTextView *textView;

- (IBAction)confirmBtnClick:(NSButton *)sender;
- (IBAction)resetBtnClick:(NSButton *)sender;


@end
