//
//  Tools.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/4/29.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "Tools.h"

BOOL SetInitDir(NSString *dirName)
{
    if( !validateString(dirName) ){
        return NO;
    }
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *pathDocuments = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    NSString *createDir = [pathDocuments stringByAppendingPathComponent:dirName];
    
    // 判断文件夹是否存在，如果不存在，则创建
    if (![fileManager fileExistsAtPath:createDir]) {
        [fileManager createDirectoryAtPath:createDir withIntermediateDirectories:YES attributes:nil error:nil];
        return YES;
    } else {
        NSLog(@"FileDir is exists.");
        return NO;
    }
}

BOOL removeFileWitName(NSString *fileName)
{
    if( ![fileName isKindOfClass:[NSString class]] ){
        return NO;
    }
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSString *pathDocuments = getMainDocumentDirPath();
    if( fileName.length > 0 ){
        pathDocuments = [pathDocuments stringByAppendingPathComponent:fileName];
    }
    NSError* error = nil;
    BOOL ret = NO;
    ret = [fileManager removeItemAtPath:pathDocuments error:&error];
    if( ret && error == nil ){
        return YES;
    }else{
        return NO;
    }
}

BOOL copyBundleFileToDocument(NSString* fileName,NSString* extName,NSString* targetDir)
{
    if( validateString(fileName) && validateString(targetDir) ){
        NSString* filePath = fileName;
        if( validateString(extName) ){
            filePath = [fileName stringByAppendingPathExtension:extName];
        }
        NSString* allPath = [targetDir stringByAppendingPathComponent:filePath];
        return copyBundleFileToDocumentWithAllpath(fileName,extName,allPath);
    }else{
        return NO;
    }
}

BOOL copyBundleFileToDocumentWithAllpath(NSString* fileName,NSString* extName,NSString* allPath)
{
    if( validateString(fileName) && validateString(allPath) ){
        if( !validateString(extName) ){
            extName = @"";
        }
        NSString* sourcePath = [[NSBundle mainBundle] pathForResource:fileName ofType:extName];
        if( !validateString(sourcePath) ){
            return NO;
        }
        if( [[NSFileManager defaultManager] fileExistsAtPath:getFilePath(allPath)] ){
            return NO;
        }else{
            return [[NSFileManager defaultManager] copyItemAtPath:sourcePath toPath:getFilePath(allPath) error:nil];
        }
        
        
    }else{
        return NO;
    }
}

NSString* getMainDocumentDirPath()
{
    NSString *pathDocuments = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    NSString *mainDir = [pathDocuments stringByAppendingPathComponent:CJFWORKKIT_DIRNAME];
    return mainDir;
}

NSString* CreatDirAndNotRemove(NSString *dirName)
{
    if( !validateString(dirName) ){
        return @"";
    }
    NSFileManager *fileManager = [[NSFileManager alloc] init];
    NSString *pathDocuments = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    NSString *createDir = [pathDocuments stringByAppendingPathComponent:[NSString stringWithFormat:@"%@/%@",CJFWORKKIT_DIRNAME,dirName]];
    
    NSString* appendName = @"_副本";
    while (YES) {
        // 判断文件夹是否存在，如果不存在，则创建
        if (![[NSFileManager defaultManager] fileExistsAtPath:createDir]) {
            [fileManager createDirectoryAtPath:createDir withIntermediateDirectories:YES attributes:nil error:nil];
            return createDir;
        } else {
            [createDir stringByAppendingString:appendName];
        }
    }
}

NSString *getFilePath(NSString* filename) {
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documentsDirectory = [paths firstObject];
    NSString *pathToUserCopyOfPlist = [documentsDirectory stringByAppendingPathComponent:[NSString stringWithFormat:@"%@/%@",CJFWORKKIT_DIRNAME, filename]];
    return pathToUserCopyOfPlist;
}

NSString *getFilePathWithExt(NSString* filename, NSString* ext) {
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *documentsDirectory = [paths firstObject];
    NSString *pathToUserCopyOfPlist = [documentsDirectory stringByAppendingPathComponent:[NSString stringWithFormat:@"%@/%@.%@",CJFWORKKIT_DIRNAME, filename, ext]];
    return pathToUserCopyOfPlist;
}


NSString *getBundleFilePath(NSString* filename, NSString* ext) {
    return [[NSBundle mainBundle] pathForResource:filename ofType:ext];
}

NSArray* getDirAllFiles(NSString* dirName,NSError** error)
{
    *error = nil;
    NSFileManager* fm = [NSFileManager defaultManager];
    if(validateString(dirName)){
        NSArray* ret = [fm contentsOfDirectoryAtPath:dirName error:error];
        if( ret && *error == nil ){
            return ret;
        }else{
            return nil;
        }
    }else{
        return nil;
    }
}

void redirectNSlogToDocumentFolder(NSString* fileName)
{
    NSString *logFilePath = getFilePath(fileName);
    // 先删除已经存在的文件
    NSFileManager *defaultManager = [NSFileManager defaultManager];
    [defaultManager removeItemAtPath:logFilePath error:nil];
    
    // 将log输入到文件
    freopen([logFilePath cStringUsingEncoding:NSASCIIStringEncoding], "a+", stdout);
    freopen([logFilePath cStringUsingEncoding:NSASCIIStringEncoding], "a+", stderr);
}

NSString* runSystemCommand(NSString *cmd,NSString* currentDir)
{
    
    NSTask* task = [[NSTask alloc] init];
    task.launchPath = @"/bin/sh";
    task.arguments = [NSArray arrayWithObjects:@"-c", cmd, nil];
    if( validateString(currentDir) ){
        task.currentDirectoryPath = currentDir;
    }
    NSPipe *pipe = [NSPipe pipe];
    [task setStandardOutput:pipe];
    [task setStandardError:pipe];
    [task launch];
    [task waitUntilExit];
    
    int status = [task terminationStatus];
    if (status == 0)
        NSLog(@"%@ Task succeeded.",cmd);
    else
        NSLog(@"%@ Task failed.",cmd);
    
    NSFileHandle *fileHandler = [pipe fileHandleForReading];
    NSData *data = [fileHandler readDataToEndOfFile];
    [fileHandler closeFile];
    
    NSString *string;
    string = [[NSString alloc]initWithData:data encoding:NSUTF8StringEncoding];
    
    return string;
}

