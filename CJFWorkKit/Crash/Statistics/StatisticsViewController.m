//
//  StatisticsViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/7/8.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "StatisticsViewController.h"
#import "CJFFileReader.h"
#import "CJFCrashDataReadManager.h"

@interface StatisticsViewController ()<CJFCrashDataReadManagerDelegate>

@property(nonatomic,strong) CJFCrashDataReadManager* manager;

@end

@implementation StatisticsViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    self.manager = [CJFCrashDataReadManager getManager];
    NSError* error = nil;
    NSArray* allFileDirs = getDirAllFiles( getFilePath(@"LocalCrashData"),&error);
    NSMutableArray* fileList = [[NSMutableArray alloc] initWithCapacity:5];
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
                    [fileList addObject:path];
                }
            }
        }
    }
    
    if( validateArray(fileList) ){
        [self.fileSelectedBtn addItemsWithTitles:fileList];
        NSString* selectedFileName = self.fileSelectedBtn.selectedItem.title;
        self.appendNameTF.stringValue = toValidateString([selectedFileName stringByDeletingPathExtension]);
    }
    [self.appNameBtn selectItemWithTitle:@"iPad"];
    self.logText.stringValue = @"本任务将对放置在 LocalCrashData下的文本文件进行提取操作。\n对于每一条crash数据，将依次完成单行内容提取 -> AES解密 -> gzip解压缩 -> 写入单独文本文件\n每个文件的命名是：uuid_随机8位字符串\n";
}

-(void)willAppendLog:( NSString*)appendStr{
    if( validateString(appendStr) ){
        self.logText.stringValue = [self.logText.stringValue stringByAppendingString:[appendStr stringByAppendingString:@"\n"]];
    }
}

//执行本地解析的解法
- (IBAction)runBtnClick:(NSButton *)sender {
    
    self.logText.stringValue = @"--------------------- log -------------------\n";
    NSString* chooseFile = self.fileSelectedBtn.selectedItem.title;
    NSString* appName = self.appNameBtn.selectedItem.title;
    NSString* targetDirName = self.appendNameTF.stringValue;
    if( validateString(appName) && validateString(chooseFile) ){
        NSDictionary* paramDic = @{@"appName":appName,
                                   @"chooseFile":chooseFile,
                                   @"targetDirName":targetDirName};
        [self.manager startReadCrashData:paramDic andReadVC:self];
        return;
    }else{
        NSString* tip = @"解析本地crash文件失败:";
        if( !validateString(appName) ){
            tip = [tip stringByAppendingString:@"appName "];
        }
        if( !validateString(chooseFile) ){
            tip = [tip stringByAppendingString:@"chooseFile "];
        }
        tip = [tip stringByAppendingString:@"is null "];
        NSLog(@"%@",tip);
        [self willAppendLog:tip];
    }
}

-(BOOL)writeCrashStringToFile:(NSString*)fileName UseCrashStr:(NSString*)crashStr andDirPath:(NSString*)dirPath
{
    if( !validateString(fileName) ){
        fileName = [NSString randomLengthString:24];
    }
    if( !validateString(dirPath) ){
        return NO;
    }
    if( !validateString(crashStr) ){
        return NO;
    }
    if( ![crashStr isEqualToString:@"exceed"] ){
        //解压缩+AES解密操作
        NSData* crashDecodeData = [crashStr dataUsingEncoding:NSUTF8StringEncoding];
        crashDecodeData = [Base64 decodeData:crashDecodeData];
        NSString* key = [@"NSObject" stringByAppendingString:@"NSString"];
        crashDecodeData = [JDGzip aes256DecryptWithData:crashDecodeData key:[key dataUsingEncoding:NSUTF8StringEncoding] iv:nil];
        crashDecodeData = [JDGzip gzipInflate:crashDecodeData];
        if( !crashDecodeData ){
            return NO;
        }
        crashStr = [[NSString alloc] initWithData:crashDecodeData encoding:NSUTF8StringEncoding];
        
        if( ![crashStr isEqualToString:@"json failure"] ){
            //json格式化及校验操作
            NSError* err = nil;
            NSDictionary* crashDic =  [NSJSONSerialization JSONObjectWithData:[crashStr dataUsingEncoding:NSUTF8StringEncoding] options:0 error:&err];
            //由于此处会存在 Number过大，无法承载的问题，会导致 JSONObjectWithData 出错
            //为了使尽可能的解析更多的crash，选择忽略这一次异常。
            if( validateDictionary(crashDic) &&  !err ){
                NSData* crashData = [NSJSONSerialization dataWithJSONObject:crashDic options:NSJSONWritingPrettyPrinted error:&err];
                if( crashData && !err ){
                    NSString* tmpStr = [[NSString alloc] initWithData:crashData encoding:NSUTF8StringEncoding];
                    if( validateString(crashStr) ){
                        crashStr = tmpStr;
                    }
                }
            }
        }
    }
    
    NSString* filePath = [dirPath stringByAppendingPathComponent:fileName];
    //文件写入操作
    NSError* err = nil;
    BOOL success = NO;
    success = [crashStr writeToFile:filePath atomically:YES encoding:NSUTF8StringEncoding error:&err];
    if( success && !err ){
        return YES;
    }else{
        return NO;
    }
}

+(NSDictionary*)convertUserInfo:(NSArray*)userInfo
{
    /*
     0 上传方式（0-老版,1-pl,2-ks）；
     1 崩溃上报时间；
     2 崩溃创建时间；
     3 平台；
     4 客户端版本；
     5 build；
     6 pin；
     7 uuid；
     8 品牌；
     9 型号；
     10 屏幕；
     11 渠道；
     12 操作系统版本；
     13 异常类型；
     14 异常代码行；
     15 堆栈；
     16 异常页面信息；
     17 异常停留页面
     */
    NSDictionary* dic = @{
                          @"upload":( userInfo.count > 0 ? userInfo[0] : @"none" ),
                          @"uploadTime":( userInfo.count > 1 ? userInfo[1] : @"none" ),
                          @"createTime":( userInfo.count > 2 ? userInfo[2] : @"none" ),
                          @"platform":( userInfo.count > 3 ? userInfo[3] : @"none" ),
                          @"version":( userInfo.count > 4 ? userInfo[4] : @"none" ),
                          @"build":( userInfo.count > 5 ? userInfo[5] : @"none" ),
                          @"pin":( userInfo.count > 6 ? userInfo[6] : @"none" ),
                          @"uuid":( userInfo.count > 7 ? userInfo[7] : @"none" ),
                          @"brand":( userInfo.count > 8 ? userInfo[8] : @"none" ),
                          @"model":( userInfo.count > 9 ? userInfo[9] : @"none" ),
                          @"screen":( userInfo.count > 10 ? userInfo[10] : @"none" ),
                          @"channel":( userInfo.count > 11 ? userInfo[11] : @"none" ),
                          @"osVerison":( userInfo.count > 12 ? userInfo[12] : @"none" ),
                          @"exceptionType":( userInfo.count > 13 ? userInfo[13] : @"none" ),
                          @"exceptionCodeLine":( userInfo.count > 14 ? userInfo[14] : @"none" ),
                          @"stack":( @"please see detail" ),
                          @"exceptionInfo":( userInfo.count > 16 ? userInfo[16] : @"none" ),
                          @"exceptionVC":( userInfo.count > 17 ? userInfo[17] : @"none" )
                          };
    return dic;
}

- (IBAction)fileSelectedBtnClick:(NSPopUpButton *)sender {
    NSString* selectedFileName = self.fileSelectedBtn.selectedItem.title;
    self.appendNameTF.stringValue = toValidateString([selectedFileName stringByDeletingPathExtension]);
}

@end
