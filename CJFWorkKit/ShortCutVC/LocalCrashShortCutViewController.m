//
//  LocalCrashShortCutViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "LocalCrashShortCutViewController.h"
#import "CJFScriptExecuteManager.h"
#import "CJFCrashDataReadManager.h"

@interface LocalCrashShortCutViewController ()

@property(nonatomic,strong) NSMutableArray* iPhoneDsymFiles;
@property(nonatomic,strong) NSMutableArray* iPadDsymFiles;
@property(nonatomic,strong) CJFCrashDataReadManager* crashReadManager;

@end

@implementation LocalCrashShortCutViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    
    self.crashReadManager = [CJFCrashDataReadManager getManager];
    
    //初始化appName和文件选择按钮
    NSError* error = nil;
    NSArray* allFiles = getDirAllFiles( getFilePath(@"LocalCrashData"),&error);
    NSMutableArray* fileList = [[NSMutableArray alloc] initWithCapacity:5];
    if( error == nil && validateArray(allFiles) ){
        for (NSString* path in allFiles) {
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
                    [fileList addObject:path];
                }
            }
        }
    }
    
    if( validateArray(fileList) ){
        [self.fileSelectedBtn addItemsWithTitles:fileList];
        NSString* selectedFileName = self.fileSelectedBtn.selectedItem.title;
        self.targetDirName.stringValue = toValidateString([selectedFileName stringByDeletingPathExtension]);
    }
    [self.appNameBtn selectItemWithTitle:@"iPad"];
    
    //初始化dsym选择器
    self.iPadDsymFiles = [[NSMutableArray alloc] initWithCapacity:5];
    self.iPhoneDsymFiles = [[NSMutableArray alloc] initWithCapacity:5];
    
    NSArray* AllDsymFiles = getDirAllFiles( getFilePath(@"SourceSymbol/self"),&error);
    if( error == nil && validateArray(AllDsymFiles) ){
        for (NSString* path in AllDsymFiles) {
            if( validateString(path) ){
                if ([[path substringToIndex:1] isEqualToString:@"."]) {
                    continue;
                }else if( [path containsString:@"xxxiPhone"] ){
                    [self.iPhoneDsymFiles addObject:path];
                }else if( [path containsString:@"xxipad"] ){
                    [self.iPadDsymFiles addObject:path];
                }
            }
        }
    }
    if( validateArray(self.iPadDsymFiles) ){
        [self.dsymSelectedBtn addItemsWithTitles:self.iPadDsymFiles];
    }
    
    //对比文件夹
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
        NSArray* compareDir = @[@"None"];
        compareDir = [compareDir arrayByAddingObjectsFromArray:fileDir];
        [self.compareSelectedBtn addItemsWithTitles:compareDir];
        [self.compareSelectedBtn selectItemWithTitle:@"None"];
    }
    
    [self willAppendLog:@"本功能是 本地提取 + 解析 + 归类 的集合，请详细填写各个参数。目录名称建议使用默认值，当然可以自己修改。Cache标识不建议勾选。对比文件夹可以为空。"];
}

-(void)willAppendLog:( NSString*)appendStr{
    if( validateString(appendStr) ){
        self.logText.string = [self.logText.string stringByAppendingString:[appendStr stringByAppendingString:@"\n"]];
    }
}

#pragma mark - 私有方法

-(BOOL)isValidParamDic:(NSDictionary*)paramDic
{
    if( validateDictionary(paramDic) &&
        validateString(paramDic[@"appName"]) &&
        validateString(paramDic[@"chooseFile"]) &&
        validateString(paramDic[@"targetDirName"]) &&
        validateString(paramDic[@"selectedFile"]) &&
        validateString(paramDic[@"version"]) &&
        validateString(paramDic[@"build"]) &&
        validateString(paramDic[@"dsymFileName"]) &&
       validateString(paramDic[@"dsymFileName"]) ){
        return YES;
    }
    return NO;
}

#pragma mark - 按钮回调

- (IBAction)runBtnClick:(NSButton *)sender
{
    self.logText.string = @"-------------------  log  -----------------\n请耐心等待所有步骤完成，在所勾选的任务完成后会有相应提示.\n";
    NSDictionary* paramDic = @{
                               @"appName":toValidateString(self.appNameBtn.selectedItem.title),
                               @"chooseFile":toValidateString(self.fileSelectedBtn.selectedItem.title),
                               @"targetDirName":toValidateString(self.targetDirName.stringValue),
                               @"selectedFile":toValidateString(self.targetDirName.stringValue),
                               @"version":toValidateString(self.versionTF.stringValue),
                               @"build":toValidateString(self.buildTF.stringValue),
                               @"dsymFileName":toValidateString(self.dsymSelectedBtn.selectedItem.title),
                               @"limitFunc":[NSString stringWithFormat:@"%ld",(long)self.advancedBtn.state],
                               @"grayFlagStr":toValidateString(self.grayValueTF.stringValue),
                               @"compareDirName":toValidateString(self.compareSelectedBtn.selectedItem.title),
                               @"firstCls":[NSString stringWithFormat:@"%ld",(long)self.firstClsBtn.state],
                               @"reCls":[NSString stringWithFormat:@"%ld",(long)self.reClsBtn.state],
                               @"finalCls":[NSString stringWithFormat:@"%ld",(long)self.finalClsBtn.state]
                               };
    @weakify(self);
    if( [self isValidParamDic:paramDic] ){
        [self.crashReadManager startReadCrashData:paramDic withCompleteBlock:^(BOOL suc) {
            @strongify(self);
            if( suc ){
                NSLog(@"文件提取成功,请等待解析......");
                [self willAppendLog:@"文件提取成功,请等待解析......"];
                
                [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptParser andParamDic:paramDic withCompleteBlock:^(NSString* result){
                    NSLog(@"%@", result);
                    [self willAppendLog:result];
                    if( [@"1" isEqualToString:paramDic[@"firstCls"]] ){
                        [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptClassifyInit andParamDic:paramDic withCompleteBlock:^(NSString *result) {
                            NSLog(@"初步分类完成：%@", result);
                            [self willAppendLog:@"初步分类完成："];
                            [self willAppendLog:result];
                            if( [@"1" isEqualToString:paramDic[@"reCls"]] ){
                                [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptClassifyRecursion andParamDic:paramDic withCompleteBlock:^(NSString *result) {
                                    NSLog(@"递归分类完成：%@", result);
                                    [self willAppendLog:@"递归分类完成："];
                                    [self willAppendLog:result];
                                    if( [@"1" isEqualToString:paramDic[@"finalCls"]] ){
                                        [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptClassifyFinal andParamDic:paramDic withCompleteBlock:^(NSString *result) {
                                            NSLog(@"最终分类完成：%@", result);
                                            [self willAppendLog:@"最终分类完成："];
                                            [self willAppendLog:result];
                                        }];
                                    }
                                }];
                            }
                            
                        }];
                    }
                    
                }];
            }else{
                NSLog(@"文件提取失败,所有任务已完成");
                [self willAppendLog:@"文件提取失败，所有任务已完成"];
            }
        }];
    }else{
        NSLog(@"参数不足");
        [self willAppendLog:@"参数不足"];
    }
}


- (IBAction)fileSelectedBtnClick:(NSPopUpButton *)sender {
    NSString* selectedFileName = self.fileSelectedBtn.selectedItem.title;
    self.targetDirName.stringValue = toValidateString([selectedFileName stringByDeletingPathExtension]);
}

- (IBAction)deviceTypeBtnClick:(NSPopUpButton *)sender {
    NSString* appName = self.appNameBtn.selectedItem.title;
    if( [appName isEqualToString:@"iPhone"] ){
        [self.dsymSelectedBtn removeAllItems];
        [self.dsymSelectedBtn addItemsWithTitles:self.iPhoneDsymFiles];
    }else{
        [self.dsymSelectedBtn removeAllItems];
        [self.dsymSelectedBtn addItemsWithTitles:self.iPadDsymFiles];
    }
}

- (IBAction)openDirBtnClick:(NSButton *)sender {
    NSString* selectedDirName = self.targetDirName.stringValue;
    if( validateString(selectedDirName) ){
        NSString* result = runSystemCommand([NSString stringWithFormat:@"open ./%@",selectedDirName], getMainDocumentDirPath());
        NSLog(@"%@",result);
        [self willAppendLog:result];
    }else{
        NSLog(@"打开目录失败：目录未选择");
        [self willAppendLog:@"打开目录失败：目录未选择"];
    }
}

- (IBAction)clsBtnClick:(NSButton *)sender {
    if( sender == self.firstClsBtn ){
        self.reClsBtn.state = sender.state;
        self.finalClsBtn.state = sender.state;
    }else if ( sender == self.reClsBtn ){
        self.finalClsBtn.state = sender.state;
    }
}

@end
