//
//  CJFFileReader.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/8/29.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFFileReader.h"

@interface CJFFileReader ()<NSStreamDelegate>

@property (strong, nonatomic) NSInputStream     *inputStream;
@property (strong, nonatomic) NSOperationQueue  *queue;
@property (strong, nonatomic) NSURL             *fileURL;
@property (strong, nonatomic) NSMutableData     *reminder;

@property (assign, nonatomic) NSInteger         lineNumber;

@property (copy, nonatomic) NSData              *delimiter;
@property (copy, nonatomic) HandleBlock         callBack;
@property (copy, nonatomic) CompletionBlock     completionBlock;

@end

@implementation CJFFileReader

- (id)initWithFileAtURL:(NSURL *)aFileURL
{
    if (![aFileURL isFileURL]) {
        return nil;
    }
    
    self = [super init];
    if (self) {
        self.fileURL = aFileURL;
        self.delimiter = [@"\n" dataUsingEncoding:NSUTF8StringEncoding];
        self.reminder = nil;
        self.lineNumber = 0;
    }
    return self;
}

- (id)initWithLocalFilePath:(NSString *)filePath
{
    if( !validateString(filePath) ){
        return nil;
    }
    self = [super init];
    if (self) {
        self.fileURL = [[NSURL alloc] initFileURLWithPath:filePath];
        self.delimiter = [@"\n" dataUsingEncoding:NSUTF8StringEncoding];
        self.reminder = nil;
        self.lineNumber = 0;
    }
    return self;
}

- (void)enumerateLinesUsingBlock:(HandleBlock)block completionBlock:(CompletionBlock)completionBlock
{
    //initial the NSOperationQueue whice can only be sequencial
    self.reminder = nil;
    self.lineNumber = 0;
    if( self.inputStream ){
        [self.inputStream close];
        self.inputStream = nil;
    }
    if (self.queue == nil) {
        self.queue = [[NSOperationQueue alloc] init];
        self.queue.maxConcurrentOperationCount = 1;
    }
    
    NSAssert(self.queue.maxConcurrentOperationCount == 1, @"Cannot read file concurrently");
    NSAssert(self.inputStream == nil, @"Cannot progress multiple input stream in parallel");
    
    self.callBack = block;
    self.completionBlock = completionBlock;
    
    //we use NSInputStream to read file
    //here the delegate should be retained(NO ARC) or the global variable(ARC)
    self.inputStream = [NSInputStream inputStreamWithURL:self.fileURL];
    self.inputStream.delegate = self;
    [self.inputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSRunLoopCommonModes];
    [self.inputStream open];
    
}

-(void)pollingNSInputStream
{
    while (1) {
        if ( [self.inputStream hasBytesAvailable] ) {
            NSMutableData *buffer = [[NSMutableData alloc] initWithLength:10 * 1024];
            NSUInteger length = (NSUInteger)[self.inputStream read:buffer.mutableBytes maxLength:buffer.length];
            if (length > 0) {
                [buffer setLength:length];
                __weak __typeof(self) weakSelf = self;
                [self.queue addOperationWithBlock:^{
                    [weakSelf processDataChunk:buffer];
                }];
            }
        }else{
            [self emitLineWithData:self.reminder];          //handle last part of data
            self.reminder = nil;
            break;
        }
    }
    
    [self.inputStream close];
    self.inputStream = nil;
    dispatch_async(dispatch_get_main_queue(), ^{
        if( self.completionBlock ){
            self.completionBlock(self.lineNumber + 1);
        }
    });
}

#pragma mark - NSStreamDelegate

- (void)stream:(NSStream *)aStream handleEvent:(NSStreamEvent)eventCode
{
    switch (eventCode) {
            
        case NSStreamEventOpenCompleted:
            break;
            
        case NSStreamEventErrorOccurred:
            NSLog(@"NSStreamEventErrorOccureed: error when reading file");
            break;
            
        case NSStreamEventEndEncountered: {
            __weak __typeof(self) weakSelf = self;
            [self.queue addOperationWithBlock:^{
                [weakSelf emitLineWithData:self.reminder];
                weakSelf.reminder = nil;
                dispatch_async(dispatch_get_main_queue(), ^{
                    if( weakSelf.completionBlock ){
                        weakSelf.completionBlock(weakSelf.lineNumber + 1);
                    }
                });
            }];
            [self.inputStream close];
            [self.inputStream removeFromRunLoop:[NSRunLoop currentRunLoop] forMode:NSRunLoopCommonModes];
            self.inputStream = nil;
            break;
        }
            
        case NSStreamEventHasBytesAvailable: {
            NSMutableData *buffer = [[NSMutableData alloc] initWithLength:10 * 1024];
            NSUInteger length = (NSUInteger)[self.inputStream read:[buffer mutableBytes] maxLength:[buffer length]];
            if (length > 0) {
                [buffer setLength:length];
                __weak __typeof(self) weakSelf = self;
                [self.queue addOperationWithBlock:^{
                    [weakSelf processDataChunk:buffer];
                }];
            }
            break;
        }
            
        default:
            break;
    }
}

- (void)emitLineWithData:(NSData *)data
{
    //get current line number
    NSUInteger lineNumber = self.lineNumber;
    //add current line number
    self.lineNumber += 1;
    
    //invoke the block to handle these data
    if (data.length > 0) {
        //get content of current line
        NSString *line = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
        dispatch_async(dispatch_get_main_queue(), ^{
            if( self.callBack ){
                self.callBack(lineNumber, line);
            }
        });
    }
}

- (void)processDataChunk:(NSMutableData *)buffer
{
    if (self.reminder == nil) {
        self.reminder = buffer;
    } else {
        //last chunk of data have some data (part of last line) reminding.
        [self.reminder appendData:buffer];
    }
    
    //separate self.reminder to lines and handle them
    [self.reminder obj_enumerateComponentsSeparatedBy:self.delimiter usingBlock:^(NSData *data, BOOL isLast) {
        
        //if it isn't last line. handle each one
        if (isLast == NO) {
            [self emitLineWithData:data];
        } else if (data.length > 0) {
            //if last line has some data reminding, save these data
            self.reminder = [data mutableCopy];
        } else {
            self.reminder = nil;
        }
    }];
}

@end
