//
//  CJFQueueManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFQueueManager.h"

static NSString* const CJFQueueNamePrefix = @"CJFQueueNamePrefix_";

@interface CJFQueueManager ()

@property(nonatomic,strong) NSMutableDictionary<NSString*, NSOperationQueue*> *myQueueList;

@end

@implementation CJFQueueManager

+(CJFQueueManager*)sharedManager
{
    static CJFQueueManager* _sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedManager = [[CJFQueueManager alloc] init];
    });
    return _sharedManager;
}

- (instancetype)init
{
    self = [super init];
    if (self) {
        self.myQueueList = [[NSMutableDictionary alloc] initWithCapacity:5];
    }
    return self;
}

#pragma mark - 对外暴露接口

-(BOOL)addOperation:(NSOperation*)operation withConcurrent:(NSInteger)threadCount andName:(NSString*)name
{
    if(  operation == nil || ![operation isKindOfClass:[NSOperation class]] ){
        return NO;
    }
    if( validateString(name) ){
        operation.name = name;
    }
    NSOperationQueue* operationQueue = [self getQueueByThreadCount:threadCount];
    [operationQueue addOperation:operation];
    return YES;
}

-(BOOL)addOperationWithBlock:(void (^)(void))block withConcurrent:(NSInteger)threadCount andName:(NSString*)name
{
    if( block == nil ){
        return NO;
    }
    NSBlockOperation* blockOperation = [NSBlockOperation blockOperationWithBlock:block];
    return [self addOperation:blockOperation withConcurrent:threadCount andName:name];
}

#pragma mark - 私有函数

-(NSOperationQueue*)getQueueByThreadCount:(NSInteger)threadCount
{
    @synchronized (self) {
        if( threadCount <= 0 ){
            threadCount = 1;
        }
        if( threadCount >= 10 ){
            threadCount = 20;
        }
        NSString* queueName = [NSString stringWithFormat:@"%@_%ld",CJFQueueNamePrefix,(long)threadCount];
        if( self.myQueueList[queueName] == nil){
            self.myQueueList[queueName] = [[NSOperationQueue alloc] init];
            self.myQueueList[queueName].maxConcurrentOperationCount = threadCount;
        }
        return self.myQueueList[queueName];
    }
}

@end
