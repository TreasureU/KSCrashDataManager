//
//  DES.h
//  Jdmobile
//
//  Created by Steven Sun on 11/11/10.
//  Copyright 2010 360buy. All rights reserved.
//

#import <Security/Security.h>
#import <CommonCrypto/CommonDigest.h>
#import <CommonCrypto/CommonCryptor.h>
#import <Foundation/Foundation.h>

@interface DES : NSObject {
    
}

+ (NSData *) doEncryptWithStringAndData:(NSString *)plainText key:(NSData *)key;

+ (NSData *) doDecryptWithStringAndData:(NSString *)cipherText key:(NSData *)key;

+ (NSData *) doEncryptWithData:(NSData *)plainData key:(NSData *)key;

+ (NSData *) doEncryptWithString:(NSString *)plainData key:(NSString *)key;

+ (NSData *) doDecryptWithData:(NSData *)cipherData key:(NSData *)key;

+ (NSData *) doDecryptWithString:(NSString *)cipherString key:(NSString *)key;

+ (NSData *) doDecryptWithData:(NSData *)cipherData keyStr:(NSString *)keyStr;

+ (NSData *) doCipher:(NSData *)plainText key:(NSData *)symmetricKey context:(CCOperation)encryptOrDecrypt padding:(CCOptions *)pkcs7;

+ (NSString*)doCipher:(NSString*)plainText key:(NSString*)key_ action:(CCOperation)encryptOrDecrypt;

@end

@interface DESManager : NSObject

+(NSString*) deDes:(NSString*)t Key:(NSString*)key;


+(NSString*) enDes:(NSString*)t Key:(NSString*)key;

@end