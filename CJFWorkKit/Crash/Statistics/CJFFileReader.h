//
//  CJFFileReader.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/8/29.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef void(^HandleBlock)(NSInteger lineNumber, NSString *line);
typedef void(^CompletionBlock)(NSInteger numberOfLines);

@interface CJFFileReader : NSObject

/**
 *  init a reader object using the URL of a file
 *
 *  @param aFileURL a NSURL object to represent a file's URL
 *
 *  @return a reader object
 */
- (id)initWithFileAtURL:(NSURL *)aFileURL;

/**
 *  init a reader object using the file's name.
 *  The file must be a local file.
 *
 *  @param filePath     local file's path
 *
 *  @return a reader object
 */
- (id)initWithLocalFilePath:(NSString *)filePath;

/**
 *  enumerate every line in file using a self-defined handle block and
 *  handle completion using a self-defined completion block
 *
 *  @param block           a block to enumerate every line and handle data
 *  @param completionBlock a block to handle completion event
 */
- (void)enumerateLinesUsingBlock:(HandleBlock)block completionBlock:(CompletionBlock) completionBlock;

@end
