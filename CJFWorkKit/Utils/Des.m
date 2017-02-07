//
//  DES.m
//  Jdmobile
//
//  Created by Steven Sun on 11/11/10.
//  Copyright 2010 360buy. All rights reserved.
//

#import "DES.h"
#import <Security/Security.h>
#import <CommonCrypto/CommonDigest.h>
#import <CommonCrypto/CommonCryptor.h>
#import "Base64.h"


#define kChosenCipherBlockSize	kCCBlockSizeDES
#define kChosenCipherKeySize	kCCKeySizeDES

//
#define kCCAlgorithm            kCCAlgorithmDES



@implementation DES


+ (NSData *) doEncryptWithData:(NSData *)plainData key:(NSData *)key {
    
    CCOptions pad = kCCOptionECBMode | kCCOptionPKCS7Padding;
//    CCOptions pad = kCCOptionECBMode;
    NSData *data = [DES doCipher:plainData key:key context:kCCEncrypt padding:&pad];
    NSData *base64Data = [Base64 encodeData:data];
    return base64Data;
    
}

/**
 key的长度必须大于等于21B.大于24B时只有前24个字节有效。
 */
+ (NSData *) doEncryptWithString:(NSString *)plainText key:(NSString *)key {
    
    NSData *plainData = [plainText dataUsingEncoding:NSUTF8StringEncoding];
    NSData *keyData = [key dataUsingEncoding:NSUTF8StringEncoding];
    return [DES doEncryptWithData:plainData key:keyData];
    
}

+ (NSData *) doEncryptWithStringAndData:(NSString *)plainText key:(NSData *)key {
    
    NSData *plainData = [plainText dataUsingEncoding:NSUTF8StringEncoding];
    return [DES doEncryptWithData:plainData key:key];
    
}

+ (NSData *) doDecryptWithStringAndData:(NSString *)cipherText key:(NSData *)key {
    
    NSData *cipherData = [cipherText dataUsingEncoding:NSUTF8StringEncoding];
    return [DES doDecryptWithData:cipherData key:key];
    
}


+ (NSData *) doDecryptWithData:(NSData *)cipherData key:(NSData *)key {
    
    CCOptions pad = kCCOptionECBMode | kCCOptionPKCS7Padding;
//    CCOptions pad = kCCOptionECBMode;
    NSData *base64Data = [Base64 decodeData:cipherData];
    NSData *data = [DES doCipher:base64Data key:key context:kCCDecrypt padding:&pad];
    return data;
    
}

/**
 key的长度必须大于等于21B.大于24B时只有前24个字节有效。
 */
+ (NSData *) doDecryptWithString:(NSString *)cipherText key:(NSString *)key {
    
    NSData *cipherData = [cipherText dataUsingEncoding:NSUTF8StringEncoding];
    NSData *keyData = [key dataUsingEncoding:NSUTF8StringEncoding];
    return [DES doDecryptWithData:cipherData key:keyData];
    
}



+ (NSData *) doDecryptWithData:(NSData *)cipherData keyStr:(NSString *)keyStr {
    
    //CCOptions pad = kCCOptionECBMode | kCCOptionPKCS7Padding;
	NSData *keyData = [keyStr dataUsingEncoding:NSUTF8StringEncoding];
	return [DES doDecryptWithData:cipherData key:keyData];
    
}



+ (NSData *) doCipher:(NSData *)plainText 
				  key:(NSData *)symmetricKey
			  context:(CCOperation)encryptOrDecrypt
			  padding:(CCOptions *)pkcs7 {
    
	//typedef int     int32_t;
    //typedef int32_t CCCryptorStatus;
	//kCCSuccess 为枚举成员 值为0;
    CCCryptorStatus ccStatus = kCCSuccess;
	//typedef struct _CCCryptor *CCCryptorRef;
    // Symmetric crypto reference.
    CCCryptorRef thisEncipher = NULL;
    // Cipher Text container.
    NSData * cipherOrPlainText = nil;
    // Pointer to output buffer.
    uint8_t * bufferPtr = NULL;
    // Total size of the buffer.
    size_t bufferPtrSize = 0;
    // Remaining bytes to be performed on.
    size_t remainingBytes = 0;
    // Number of bytes moved to buffer.
    size_t movedBytes = 0;
    // Length of plainText buffer.
    size_t plainTextBufferSize = 0;
    // Placeholder for total written.
    size_t totalBytesWritten = 0;
    // A friendly helper pointer.
    uint8_t * ptr;
    
    // Initialization vector; dummy in this case 0's.
    uint8_t iv[kChosenCipherBlockSize];
    memset((void *) iv, 0x0, (size_t) sizeof(iv));
    
    
    if (plainText == nil) {
//        NSLog(@"PlainText object cannot be nil.");
    }
    
    
    
    if (symmetricKey == nil) {
//        NSLog(@"Symmetric key object cannot be nil.");
    }
    
    
    if (pkcs7 == NULL) {
//        NSLog(@"CCOptions * pkcs7 cannot be NULL.");
    }
    
    if ([symmetricKey length] != kChosenCipherKeySize) {
//        NSLog(@"Disjoint choices for key size." );
    }
    
    plainTextBufferSize = [plainText length];
    
    if (plainTextBufferSize <= 0) {
//        NSLog(@"Empty plaintext passed in." );
    }
    
    // We don't want to toss padding on if we don't need to
    //if(encryptOrDecrypt == kCCEncrypt) {
	//        if(*pkcs7 != kCCOptionECBMode) {
	//            if((plainTextBufferSize % kChosenCipherBlockSize) == 0) {
	//                *pkcs7 = 0x0000;
	//            } else {
	//                *pkcs7 = kCCOptionPKCS7Padding;
	//            }
	//        }
	//    } else if(encryptOrDecrypt != kCCDecrypt) {
	//        //LOGGING_FACILITY1( 0, @"Invalid CCOperation parameter [%d] for cipher context.", *pkcs7 );
	//        ZNLog(@"Invalid CCOperation parameter [%d] for cipher context.", *pkcs7);
	//    } 
    
    
    
    // Create and Initialize the crypto reference.
    if( pkcs7 != NULL )
        ccStatus = CCCryptorCreate(	encryptOrDecrypt,
                                   kCCAlgorithm,
                                   *pkcs7,
                                   (const void *)[symmetricKey bytes],
                                   kChosenCipherKeySize,
                                   (const void *)iv,
                                   &thisEncipher
                                   );
    
    
    if (ccStatus != kCCSuccess) {
        NSLog(@"Problem creating the context, ccStatus == %d.", ccStatus);
    }
    
    // Calculate byte block alignment for all calls through to and including final.
    bufferPtrSize = CCCryptorGetOutputLength(thisEncipher, plainTextBufferSize, true);
    
    // Allocate buffer.
    bufferPtr = malloc( bufferPtrSize * sizeof(uint8_t) );
    
    // Zero out buffer.
    memset((void *)bufferPtr, 0x0, bufferPtrSize);
    
    // Initialize some necessary book keeping.
    
    ptr = bufferPtr;
    
    // Set up initial size.
    remainingBytes = bufferPtrSize;
    
    // Actually perform the encryption or decryption.
    ccStatus = CCCryptorUpdate( thisEncipher,
                               (const void *) [plainText bytes],
                               plainTextBufferSize,
                               ptr,
                               remainingBytes,
                               &movedBytes
                               );
    
    
    if (ccStatus != kCCSuccess) {
        NSLog(@"Problem with CCCryptorUpdate, ccStatus == %d.", ccStatus);
    }
    
    // Handle book keeping.
    ptr += movedBytes;
    remainingBytes -= movedBytes;
    totalBytesWritten += movedBytes;
    
    // Finalize everything to the output buffer.
    ccStatus = CCCryptorFinal(thisEncipher,
                              ptr,
                              remainingBytes,
                              &movedBytes
                              );
    
    
    
    totalBytesWritten += movedBytes;
    
    if(thisEncipher) {
        (void) CCCryptorRelease(thisEncipher);
        thisEncipher = NULL;
    }
    
    
    if (ccStatus != kCCSuccess) {
        NSLog(@"Problem with encipherment ccStatus == %d", ccStatus);
    }
    
    cipherOrPlainText = [NSData dataWithBytes:(const void *)bufferPtr length
											 :(NSUInteger)totalBytesWritten];
    
    if(bufferPtr) free(bufferPtr);
    
    return cipherOrPlainText;
    
}

+ (NSString*)doCipher:(NSString*)plainText 
				  key:(NSString*)key_
			   action:(CCOperation)encryptOrDecrypt { 
	const void *vplainText;
	size_t plainTextBufferSize;
	
	if (encryptOrDecrypt == kCCDecrypt) {
		NSData *EncryptData = [Base64 decodeString:plainText];
		plainTextBufferSize = [EncryptData length];
		vplainText = [EncryptData bytes];
	}
	else {
		//plainTextBufferSize = [plainText length];
		//vplainText = (const void *)[plainText UTF8String];
		
		NSData *plainTextData = [plainText dataUsingEncoding: NSUTF8StringEncoding]; 
		plainTextBufferSize = [plainTextData length]; 
		vplainText = [plainTextData bytes];
	}
	
	CCCryptorStatus ccStatus;
	uint8_t *bufferPtr = NULL;
	size_t bufferPtrSize = 0;
	size_t movedBytes = 0;
 	
	bufferPtrSize = (plainTextBufferSize + kCCBlockSize3DES) & ~(kCCBlockSize3DES - 1);
	bufferPtr = malloc( bufferPtrSize * sizeof(uint8_t));
	memset((void *)bufferPtr, 0x0, bufferPtrSize);
	// memset((void *) iv, 0x0, (size_t) sizeof(iv));
	
	NSString *key = key_; 
 	const void *vkey = (const void *)[key UTF8String];
 	
	ccStatus = CCCrypt(encryptOrDecrypt,
					   kCCAlgorithmDES,
					   kCCOptionECBMode | kCCOptionPKCS7Padding,
					   vkey, //"123456789012345678901234", //key
					   kCCKeySizeDES,
					   nil, //"init Vec", //iv,
					   vplainText, //"Your Name", //plainText,
					   plainTextBufferSize,
					   (void *)bufferPtr,
					   bufferPtrSize,
					   &movedBytes);
    
    if (ccStatus == kCCParamError){
        free(bufferPtr);
        return @"PARAM ERROR";
    }
    else if (ccStatus == kCCBufferTooSmall) {
        free(bufferPtr);
        return @"BUFFER TOO SMALL";
    }
    else if (ccStatus == kCCMemoryFailure){
        free(bufferPtr);
        return @"MEMORY FAILURE";
    }
    else if (ccStatus == kCCAlignmentError) {
        free(bufferPtr);
        return @"ALIGNMENT";
    }
    else if (ccStatus == kCCDecodeError){
        free(bufferPtr);
        return @"DECODE ERROR";
    }
    else if (ccStatus == kCCUnimplemented) {
        free(bufferPtr);
        return @"UNIMPLEMENTED";
    }
	
	NSString *result;
	
	if (encryptOrDecrypt == kCCDecrypt) {
		result = [[[NSString alloc] initWithData:[NSData dataWithBytes:(const void *)bufferPtr 
																length:(NSUInteger)movedBytes] 
										encoding:NSUTF8StringEncoding] autorelease];
	}
	else {
		NSData *myData = [NSData dataWithBytes:(const void *)bufferPtr length:(NSUInteger)movedBytes];
		result = [Base64 stringByEncodingData:myData];
	}
    free( bufferPtr );
	return result; 
}


@end

@implementation DESManager

+(NSString*) deDes:(NSString*)t Key:(NSString*)key
{
    NSData *decData = [DES doDecryptWithString:t key:key];
    NSString *decStr = [[[NSString alloc] initWithData:decData encoding:NSUTF8StringEncoding] autorelease];
    return decStr;
}

+(NSString*) enDes:(NSString*)t Key:(NSString*)key
{
    NSData *encData = [DES doEncryptWithString:t key:key];
    NSString *encStr = [[[NSString alloc] initWithData:encData encoding:NSUTF8StringEncoding] autorelease];
    return encStr;
}

@end