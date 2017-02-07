//
//  CJFQueueManager.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface CJFQueueManager : NSObject

+(CJFQueueManager*)sharedManager;

-(BOOL)addOperation:(NSOperation*)operation withConcurrent:(NSInteger)threadCount andName:(NSString*)name;
-(BOOL)addOperationWithBlock:(void (^)(void))block withConcurrent:(NSInteger)threadCount andName:(NSString*)name;

@end
