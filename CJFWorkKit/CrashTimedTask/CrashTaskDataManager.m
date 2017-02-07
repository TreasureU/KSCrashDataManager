//
//  CrashTaskDataManager.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/13.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CrashTaskDataManager.h"

static NSString* const SCrashFileName = @"Setting/crashDataFile";

@implementation CrashTaskDataManager{
    NSMutableArray<CrashTimedModel*> *_realArr;
}

- (instancetype)init
{
    self = [super init];
    if (self) {
        _realArr = [NSKeyedUnarchiver unarchiveObjectWithFile:getFilePath(SCrashFileName)];
        if( !_realArr ){
            _realArr = [[NSMutableArray alloc] initWithCapacity:5];
        }
    }
    return self;
}

+(CrashTaskDataManager*)sharedManager
{
    static CrashTaskDataManager* _sharedManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        _sharedManager = [[CrashTaskDataManager alloc] init];
    });
    return _sharedManager;
}

-(NSArray*)crashArr
{
    return [_realArr copy];
}

-(BOOL)checkFileName:(NSString*)fileName
{
    if( !validateString(fileName) ){
        return NO;
    }
    @synchronized (self) {
        for (CrashTimedModel* model in _realArr) {
            if([model.fileNameLab isEqualToString:fileName]){
                return NO;
            }
        }
        return YES;
    }
}

-(BOOL)addCrashModel:(CrashTimedModel*)model
{
    @synchronized (self) {
        [self deleteCrashModelByName:model.fileNameLab];
        [_realArr addObject:model];
        [self saveData];
        return YES;
    }
}

-(BOOL)deleteCrashModelByName:(NSString*)fileName
{
    if( !fileName ){
        return NO;
    }
    
    @synchronized (self) {
        NSMutableArray* arr = [[NSMutableArray alloc] initWithCapacity:5];
        for (CrashTimedModel* model in _realArr ) {
            if( ![model.fileNameLab isEqualToString:fileName] ){
                [arr addObject:model];
            }
        }
        _realArr = arr;
        [self saveData];
        return YES;
    }
}

-(BOOL)removeAllData
{
    @synchronized (self) {
        [_realArr removeAllObjects];
        [self saveData];
        return  YES;
    }
}

-(BOOL)saveData
{
    NSString* path = getFilePath(SCrashFileName);
    return [NSKeyedArchiver archiveRootObject:_realArr toFile:path];
}

@end
