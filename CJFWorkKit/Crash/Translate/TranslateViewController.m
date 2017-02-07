//
//  TranslateViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "TranslateViewController.h"
#import "CJFScriptExecuteManager.h"

@interface TranslateViewController ()

@end

@implementation TranslateViewController

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
    self.logText.string = @"请使用命令: python JDiOSOOMClassify.py <iPad/iPhone> <fileDir> <BG/AT/IA/FG/None>\n脚本将自动解析指定目录下的 *.json 文件,请将 KCrash解析后的数据放置在里面.\n脚本执行所在目录默认为脚本所在目录,注意文件夹位置关系。\n如果需要调试代码,直接使用 cmd+R 运行,需要将 target_debug_flag 置为 True\n";
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
    NSString* OOMName = self.OOMSelectedBtn.selectedItem.title;
    NSString* sourceDir = [@"oom" stringByAppendingPathComponent:OOMName];
    NSString* targetDir = [sourceDir stringByAppendingString:@"_Report"];
    if( validateString(appName) && validateString(selectedFile) && validateString(OOMName) ){
        __weak __typeof(self) weakSelf = self;
        NSDictionary* paramDic = @{
                                   @"appName":appName,
                                   @"selectedFile":selectedFile,
                                   @"sourceDir":sourceDir,
                                   @"targetDir":targetDir
                                   };
        [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptOOMClassify andParamDic:paramDic withCompleteBlock:^(NSString *result) {
            [weakSelf willAppendLog:result];
            if( validateString(result) ){
                NSLog(@"%@",result);
            }
        }];
    }else{
        NSLog(@"it is run parser script error");
        [self willAppendLog:@"it is run parser script error"];
    }
}
@end
