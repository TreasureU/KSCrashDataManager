//
//  ClassifyViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "ClassifyViewController.h"
#import "CJFScriptExecuteManager.h"


@interface ClassifyViewController ()

@end

@implementation ClassifyViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    NSArray* jsonArray = @[@"初步分类",
                           @"递归分类",
                           @"合并报表"];
    if( validateArray(jsonArray) ){
        [self.scriptBtn addItemsWithTitles:jsonArray];
    }
    
    // Do view setup here.
    NSError* error = nil;
    NSArray* allFileDirs = getDirAllFiles( getMainDocumentDirPath(),&error);
    NSMutableArray* fileDir = [[NSMutableArray alloc] initWithCapacity:5];
    if( error == nil && validateArray(allFileDirs) ){
        for (NSString* path in allFileDirs) {
            if( validateString(path) ){
                if ([[path substringToIndex:1] isEqualToString:@"."]) {
                    continue;
                }else if ([path isEqualToString:@"ParserScript"]) {
                    continue;
                }else if ([path isEqualToString:@"Setting"]) {
                    continue;
                }else if ([path isEqualToString:@"SourceSymbol"]) {
                    continue;
                }else if ([path isEqualToString:@"LocalCrashData"]) {
                    continue;
                }else {
                    [fileDir addObject:path];
                }
            }
        }
    }
    
    if( validateArray(fileDir) ){
        [self.fileSelectedBtn addItemsWithTitles:fileDir];
        NSArray* compareDir = @[@"None"];
        compareDir = [compareDir arrayByAddingObjectsFromArray:fileDir];
        [self.compareSelectedBtn addItemsWithTitles:compareDir];
        [self.compareSelectedBtn selectItemWithTitle:@"None"];
    }
    [self.appNameBtn selectItemWithTitle:@"iPad"];
    self.logText.string = @"本功能一共分为三个脚本完成：\n1.初步分类：按照symbol和controller归类crash数据。\n2.递归分类：用户可以自己配置crash匹配表，然后分类到system下面。\n3.合并报表：对前面的输出报告做统一，输出FinalResult和Reports\n";
}

-(void)willAppendLog:( NSString*)appendStr{
    if( validateString(appendStr) ){
        self.logText.string = [self.logText.string stringByAppendingString:[appendStr stringByAppendingString:@"\n"]];
    }
}

- (IBAction)runBtnClick:(NSButton *)sender {
    self.logText.string = @"--------------------- log -------------------\n";
    NSString* selectedFile = self.fileSelectedBtn.selectedItem.title;
    NSString* appName = self.appNameBtn.selectedItem.title;
    NSString* scriptName = self.scriptBtn.selectedItem.title;
    NSString* compareDirName = self.compareSelectedBtn.selectedItem.title;
    if( validateString(appName) && validateString(selectedFile) ){
        if(!validateString(compareDirName)){
            compareDirName = @"";
        }
        NSLog(@"will begin run classify script");
        [self willAppendLog:@"will begin run classify script"];
        
        __weak __typeof(self) weakSelf = self;
        NSDictionary* paramDic = @{
                                   @"appName":appName,
                                   @"selectedFile":selectedFile,
                                   @"compareDirName":compareDirName
                                   };
        CJFScriptType scriptType = CJFScriptNone;
        if( [scriptName isEqualToString:@"递归分类"] ){
            scriptType = CJFScriptClassifyRecursion;
        }else if ( [scriptName isEqualToString:@"合并报表"] ){
            scriptType = CJFScriptClassifyFinal;
        }else{
            scriptType = CJFScriptClassifyInit;
        }
        [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:scriptType andParamDic:paramDic withCompleteBlock:^(NSString *result) {
            [weakSelf willAppendLog:result];
            if( validateString(result) ){
                NSLog(@"%@",result);
            }
            NSLog(@"run classify script is done.");
            [weakSelf willAppendLog:@"run classify script is done."];
        }];
    }else{
        NSLog(@"it is run classify script error");
        [self willAppendLog:@"it is run classify script error"];
    }
}

- (IBAction)openDirBtnClick:(NSButton *)sender {
    NSString* selectedDirName = self.fileSelectedBtn.selectedItem.title;
    if( validateString(selectedDirName) ){
        NSString* result = runSystemCommand([NSString stringWithFormat:@"open ./%@",selectedDirName], getMainDocumentDirPath());
        NSLog(@"%@",result);
        [self willAppendLog:result];
    }else{
        NSLog(@"打开目录失败：目录未选择");
        [self willAppendLog:@"打开目录失败：目录未选择"];
    }
}

@end
