//
//  ExcelViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "ExcelViewController.h"
#import "CJFScriptExecuteManager.h"

@interface ExcelViewController ()

@end

@implementation ExcelViewController

- (void)viewDidLoad {
    [super viewDidLoad];
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
    }
    [self.appNameBtn selectItemWithTitle:@"iPad"];
    self.logText.string = @"请使用命令: python JDiOSExcelFromDir.py <iPad/iPhone> <fileDirs,....>\n对指定文件夹下的所有json文件进行递归查找并且添加到相应的list中,最后归类到相应的表格中\n文件输出名字:dirName.xlsx\n";
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
    NSString* subDirStrs = self.subDirPathList.stringValue;
    NSArray* subDirList = [subDirStrs componentsSeparatedByString:@";"];
    if( validateString(appName) && validateString(selectedFile) && validateArray(subDirList)){
        NSLog(@"will begin run parser script.This Script is very slow ,Please waiting …………");
        NSString* pathStr = @"";
        for (NSString* subPath in subDirList) {
            if( pathStr.length > 0 ){
                pathStr = [pathStr stringByAppendingString:@" "];
            }
            pathStr = [pathStr stringByAppendingString:[NSString stringWithFormat:@"../%@/%@",selectedFile,subPath]];
        }
        [self willAppendLog:@"will begin run parser script.This Script is very slow ,Please waiting …………"];
        __weak __typeof(self) weakSelf = self;
        
        NSDictionary* paramDic = @{
                                   @"appName":appName,
                                   @"pathStr":pathStr,
                                   };
        [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptExcel andParamDic:paramDic withCompleteBlock:^(NSString *result) {
            result = toValidateString(result);
            [weakSelf willAppendLog:result];
            NSLog(@"%@",result);
            [weakSelf willAppendLog:@"解析完成"];
        }];
    }else{
        NSLog(@"it is run Excel script error");
        [self willAppendLog:@"it is run Excel script error"];
    }
}
@end
