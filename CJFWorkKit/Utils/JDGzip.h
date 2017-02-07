//
//  JDGzip.h
//  MA
//
//  Created by ChengJianFeng on 16/7/21.
//  Copyright (c) 2016年 360Buy. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface JDGzip : NSObject

//解压缩
+ (NSData *)gzipInflate:(NSData*)data;
//压缩
+ (NSData *)gzipDeflate:(NSData*)data;

//AES加密
+ (NSData *)aes256EncryptWithData:(NSData*)data  Key:(NSData *)key iv:(NSData *)iv;

//AES解密
+ (NSData *)aes256DecryptWithData:(NSData*)data key:(NSData *)key iv:(NSData *)iv;

@end
