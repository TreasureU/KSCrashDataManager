//
//  CrashViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/6/22.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CrashViewController.h"
#import "CJFNetworkManager.h"

static NSString* const CJF_CrashGetRemoteCache = @"CJF_CrashGetRemoteCache";

@interface CrashViewController ()

@end

@implementation CrashViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    NSDictionary* paramDic = [[NSUserDefaults standardUserDefaults] objectForKey:CJF_CrashGetRemoteCache];
    if( validateDictionary(paramDic) ){
        NSString* client = toValidateString(paramDic[@"client"]);
        if( [@"iPad" isEqualToString:client] || [@"apple" isEqualToString:client] ){
            [self.clientChoiceBtn selectItemWithTitle:client];
        }else{
            [self.clientChoiceBtn selectItemWithTitle:@"iPad"];
        }
        self.versionLab.stringValue = toValidateString(paramDic[@"clientVersion"]);
        self.buildLab.stringValue = toValidateString(paramDic[@"build"]);
        self.UUIDLab.stringValue = toValidateString(paramDic[@"uuid"]);;
        self.userNameLab.stringValue = toValidateString(paramDic[@"pin"]);
        self.pipeLab.stringValue = toValidateString(paramDic[@"partner"]);
        self.fileNameLab.stringValue = toValidateString(paramDic[@"fileName"]);
    }else{
        [self.clientChoiceBtn selectItemWithTitle:@"iPad"];
    }
    self.crashStartLab.stringValue = [[NSDate date] getCrashDateStyleStirng];
    self.crashEndLab.stringValue = [self.crashStartLab.stringValue stringByReplacingCharactersInRange:NSMakeRange(11, 8) withString:@"23:59:59"];
    
    self.logText.string = @"--------------------- log -------------------\n由于后台更新，所有网络相关功能都已废弃，仅留下基础的网络框架。";
}

- (IBAction)confirmBtnClick:(NSButton *)sender {
    //如果有校验，请提前在此处完成
    self.logText.string = @"--------------------- log -------------------\n";
    NSDictionary* paramDic = @{
        @"client":self.clientChoiceBtn.selectedItem.title,
        @"clientVersion":self.versionLab.stringValue,
        @"build":self.buildLab.stringValue,
        @"uuid":self.UUIDLab.stringValue,
        @"pin":self.userNameLab.stringValue,
        @"partner":self.pipeLab.stringValue,
        @"startTime":self.crashStartLab.stringValue,
        @"endTime":self.crashEndLab.stringValue,
        @"fileName":self.fileNameLab.stringValue
    };
    [[NSUserDefaults standardUserDefaults] setObject:paramDic forKey:CJF_CrashGetRemoteCache];
    [GetRemoteCrashDataManager getOperationCookie:paramDic andVC:self];
}

- (IBAction)resetBtnClick:(NSButton *)sender {
    [self.clientChoiceBtn selectItemWithTitle:@"iPad"];
    self.versionLab.stringValue = @"";
    self.buildLab.stringValue = @"";
    self.UUIDLab.stringValue = @"";
    self.userNameLab.stringValue = @"";
    self.pipeLab.stringValue = @"";
    self.fileNameLab.stringValue = @"";
    self.logText.string = @"--------------------- log -------------------\n";
}

@end
