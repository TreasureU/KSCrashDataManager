//
//  ParserViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "ParserViewController.h"
#import "CJFScriptExecuteManager.h"

@interface ParserViewController ()

@property(nonatomic,strong) NSMutableArray* iPadDsymFiles;
@property(nonatomic,strong) NSMutableArray* iPhoneDsymFiles;

@end

@implementation ParserViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    self.advancedBtn.state = 1;
    
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
    
    
    [self.appNameBtn selectItemWithTitle:@"iPad"];
    self.logText.string = @"在第二排的第一个框需要输入CFBundleShortVersionString，iPad类似于3.9.0，iPhone类似于5.4.1，第二框需要输入CFBundleVersion，iPad类似于8050，iPhone类似于122445.由于iPhone的build号和version是反的，导致灰度时不能修改两者，无法区分是第几次灰度的崩溃，因此，需要额外指定灰度标识。注意，在线上版本或者非灰度版本中，请将该字段置为空。目前精简版和高级版的功能已经一体化，如果在sourceSymbol的arm64、armv7、armv7s这里个文件夹下，存在按照“库名_系统”命名的系统符号表，例如CoreFoundation_6.1.2，那么程序会自动解析到，并载入该文件参与解析。请不要轻易勾选cache功能，除非你非常确定自己的“符号表文件名_version_build”从来没有重复过。 否则虽然可以加快速度，但是会导致错误的解析结果\n";
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
    NSString* build = self.buildTF.stringValue;
    NSString* version = self.versionTF.stringValue;
    NSString* dsymFileName = self.dsymSelectedBtn.selectedItem.title;
    NSString* grayFlagStr = @"";
    if( [appName isEqualToString:@"iPhone"] ){
        grayFlagStr = self.grayValueTF.stringValue;
    }
    
    if( validateString(appName) && validateString(selectedFile) && validateString(build) && validateString(version) && validateString(dsymFileName)){
        NSLog(@"will begin run parser script.This Script is very slow ,Please waiting …………");
        [self willAppendLog:@"will begin run parser script.This Script is very slow ,Please waiting …………"];
        __weak __typeof(self) weakSelf = self;
        
        NSDictionary* paramDic = @{
                                   @"appName":appName,
                                   @"selectedFile":selectedFile,
                                   @"version":version,
                                   @"build":build,
                                   @"dsymFileName":dsymFileName,
                                   @"limitFunc":[NSString stringWithFormat:@"%ld",(long)self.advancedBtn.state],
                                   @"grayFlagStr":grayFlagStr
                                   };
        BOOL ret =  [[CJFScriptExecuteManager sharedManager] asyncExcuteScript:CJFScriptParser andParamDic:paramDic withCompleteBlock:^(NSString *result) {
            [weakSelf willAppendLog:result];
            if( validateString(result) ){
                NSLog(@"%@",result);
            }
        }];
        if( ret == NO ){
            NSLog(@"解析失败，请检查原因");
            [self willAppendLog:@"解析失败，请检查原因"];
        }
        
    }else{
        NSLog(@"解析程序参数不足");
        [self willAppendLog:@"解析程序参数不足"];
    }
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

- (IBAction)openDirBtnCilck:(NSButton *)sender {
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
