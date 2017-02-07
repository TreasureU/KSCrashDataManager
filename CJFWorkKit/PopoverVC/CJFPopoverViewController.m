//
//  CJFPopoverViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/22.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFPopoverViewController.h"
#import "CJFInitManager.h"
#import "CJFWindowManager.h"

@interface CJFPopoverViewController ()

@end

@implementation CJFPopoverViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
}

- (IBAction)scriptRecoverBtnClick:(NSButton *)sender {
    [[CJFInitManager sharedManager] forceScriptFileReplace];
}

- (IBAction)environmentRecoverBtnClick:(NSButton *)sender {
    [[CJFInitManager sharedManager] rebuildEnvironment];
}


- (IBAction)openCacheDirBtnClick:(NSButton *)sender {
    NSString* sourcePath = getFilePath(@"ParserScript/cache");
    if( validateString(sourcePath) ){
        NSString* result = runSystemCommand([NSString stringWithFormat:@"open %@",sourcePath], getMainDocumentDirPath());
        NSLog(@"打开 cache 目录结果：%@",result);
    }
}

- (IBAction)openRulesBtnClick:(NSButton *)sender {
    NSString* sourcePath = getFilePath(@"ParserScript/setting");
    if( validateString(sourcePath) ){
        NSString* result = runSystemCommand([NSString stringWithFormat:@"open %@",sourcePath], getMainDocumentDirPath());
        NSLog(@"打开 rules 目录结果：%@",result);
    }
}

- (IBAction)openDsymPanelBtnClick:(NSButton *)sender {
    [[CJFWindowManager sharedManager] presentNewWindowWithName:FN_QuicklyImport];
}


- (IBAction)openCrashTxtBtnClick:(NSButton *)sender {
    NSString* sourcePath = getFilePath(@"LocalCrashData");
    if( validateString(sourcePath) ){
        NSString* result = runSystemCommand([NSString stringWithFormat:@"open %@",sourcePath], getMainDocumentDirPath());
        NSLog(@"打开 rules 目录结果：%@",result);
    }
}


@end
