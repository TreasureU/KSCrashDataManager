//
//  CrashAccountViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/12/6.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CrashAccountViewController.h"
#import "GetRemoteCrashDataManager.h"

@interface CrashAccountViewController ()

@end

@implementation CrashAccountViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    if( validateString([[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetAccountKey]) && validateString([[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetPasswordKey]) ){
        self.accountTextFiled.stringValue = [[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetAccountKey];
        self.passwordTextField.stringValue = [[NSUserDefaults standardUserDefaults] objectForKey:JDCrashGetPasswordKey];
    }
    self.textView.string = @"输出自己的账号密码，然后点击confirm。程序会去尝试登录流程以此来校验账号密码，如果校验正确，那么会将账号密码记录到硬盘备用，否则，账号密码是无效的。点击reset，不仅会清空界面上的内容，而且会将之前记录到硬盘的账号密码都清空。当硬盘上没有存储账号密码时，将默认使用chengjianfeng的账号密码。【验证代码已废弃】\n";
    
}

-(void)willAppendLog:( NSString*)appendStr{
    if( validateString(appendStr) ){
        self.textView.string = [self.textView.string stringByAppendingString:[appendStr stringByAppendingString:@"\n"]];
    }
}


- (IBAction)confirmBtnClick:(NSButton *)sender {
    self.textView.string = @"------ log -------\n";
    
    NSString* account = self.accountTextFiled.stringValue;
    NSString* password = self.passwordTextField.stringValue;
    
    [[NSUserDefaults standardUserDefaults] setObject:account forKey:JDCrashGetAccountKey];
    [[NSUserDefaults standardUserDefaults] setObject:password forKey:JDCrashGetPasswordKey];
    [self willAppendLog:@"添加成功"];
}

- (IBAction)resetBtnClick:(NSButton *)sender {
    [[NSUserDefaults standardUserDefaults] removeObjectForKey:JDCrashGetAccountKey];
    [[NSUserDefaults standardUserDefaults] removeObjectForKey:JDCrashGetPasswordKey];
    self.accountTextFiled.stringValue = @"";
    self.passwordTextField.stringValue = @"";
}
@end
