//
//  NSData+Sperate.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/8/29.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef void(^EnumerateBlock)(NSData* data,BOOL hasLine);

@interface NSData(Sperate)

- (void)obj_enumerateComponentsSeparatedBy:(NSData *)delimiter usingBlock:(EnumerateBlock)block;

@end
