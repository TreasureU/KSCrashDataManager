//
//  Tools.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/4/29.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef NS_ENUM(NSUInteger, CJFSymBolType) {
    CJFSymBolUIKit,
    CJFSymBollibobjc,
    CJFSymBolCoreFoundation,
    CJFSymBolSelf
};

//该方法仅用于赋初值时使用
static inline NSString *toValidateString(NSString *string) {
    bool result = false;
    if (string && [string isKindOfClass:[NSString class]] && [string length]) {
        result = true;
    }
    return result ? string : @"";
}

static inline bool validateString(NSString *string) {
    bool result = false;
    if (string && [string isKindOfClass:[NSString class]] && [string length]) {
        result = true;
    }
    return result;
}

//该方法仅用于赋初值时使用
static inline NSArray *toValidateArray(NSArray *array) {
    bool result = false;
    if (array && [array isKindOfClass:[NSArray class]] && [array count]) {
        result = true;
    }
    return result ? array : @[];
}

static inline bool validateArray(NSArray *array) {
    bool result = false;
    if (array && [array isKindOfClass:[NSArray class]] && [array count]) {
        result = true;
    }
    return result;
}

//该方法仅用于赋初值时使用
static inline NSNumber *toValidateNumber(NSNumber *number) {
    bool result = false;
    if (number && [number isKindOfClass:[NSNumber class]]) {
        result = true;
    }
    
    return result ? number : @0;
}

static inline bool validateNumber(NSNumber *number) {
    bool result = false;
    if (number && [number isKindOfClass:[NSNumber class]]) {
        result = true;
    }
    return result;
}

//该方法仅用于赋初值时使用
static inline NSDictionary *toValidateDictionary(NSDictionary *dictionary) {
    bool result = false;
    if (dictionary && [dictionary isKindOfClass:[NSDictionary class]]) {
        result = true;
    }
    return result ? dictionary : @{};
}

static inline bool validateDictionary(NSDictionary *dictionary) {
    bool result = false;
    if (dictionary && [dictionary isKindOfClass:[NSDictionary class]]) {
        result = true;
    }
    return result;
}

/**
 *  @brief  处理成string类型
 *
 *  @param obj 传入number或string对象 其他的对象类型则直接返回空
 *
 *  @return 处理后的字符串
 */
static inline NSString *numberToString(id obj) {
    if ([obj isKindOfClass:[NSNumber class]] || [obj isKindOfClass:[NSString class]]) {
        NSString *string = [NSString stringWithFormat:@"%@", obj];
        return string;
    } else {
        return @"";
    }
}

static inline NSString *timeString(double timeSec) {
    NSDateComponents *dateComponents = [[NSCalendar currentCalendar] components:(NSCalendarUnitHour | NSCalendarUnitMinute | NSCalendarUnitSecond) fromDate:[NSDate dateWithTimeIntervalSinceReferenceDate:0] toDate:[NSDate dateWithTimeIntervalSinceReferenceDate:timeSec] options:0];
    
    NSInteger hours = [dateComponents hour];
    NSInteger minutes = [dateComponents minute];
    NSInteger seconds = [dateComponents second];
    
    NSString *time = [NSString stringWithFormat:@"%li:%li:%li", (long) hours, (long) minutes, (long) seconds];
    return time;
}

/**
 *  获取文件路径的函数
 *
 *  @param filename 文件名
 *  @param ext      扩展名
 *
 *  @return 文件路径
 */
BOOL SetInitDir(NSString *dirName);


/**
 删除主文件夹下的指定文件，可以删除非空文件夹。传入空串可以删除整个文件夹。

 @param fileName 相对路径
 @return 删除操作执行结果
 */
BOOL removeFileWitName(NSString *fileName);

/**
 将bundle中的指定文件copy到Document目录下,不支持覆盖创建

 @param fileName 文件名
 @param extName 扩展名
 @param targetDir Document下的相对路径，不包含目标文件名，注意，一定是在CJFWORKKIT下
 @return 成功与否
 */
BOOL copyBundleFileToDocument(NSString* fileName,NSString* extName,NSString* targetDir);
BOOL copyBundleFileToDocumentWithAllpath(NSString* fileName,NSString* extName,NSString* allPath);
NSString* getMainDocumentDirPath();
NSString* CreatDirAndNotRemove(NSString *dirName);
NSString *getFilePath(NSString *filename);
NSString *getFilePathWithExt(NSString* filename, NSString* ext);
NSString *getBundleFilePath(NSString* filename, NSString* ext);

/**
 *  获取一个文件夹下所有文件
 *
 *  @param dirName 文件名
 *  @param error
 *
 *  @return
 */
NSArray* getDirAllFiles(NSString* dirName,NSError** error);

/**
 *  重定向输出到log日志
 *
 *  @param fileName 文件名
 */
void redirectNSlogToDocumentFolder(NSString* fileName);

/**
 *  代码执行shell命令
 *
 *  @param cmd        需要执行的指令
 *  @param currentDir 执行指令时的文件夹路径
 */
NSString* runSystemCommand(NSString *cmd, NSString* currentDir);
