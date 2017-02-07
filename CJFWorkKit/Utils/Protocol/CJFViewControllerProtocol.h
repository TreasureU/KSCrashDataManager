//
//  CJFViewControllerProtocol.h
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import <Cocoa/Cocoa.h>

#ifndef CJFViewControllerProtocol_h
#define CJFViewControllerProtocol_h

@protocol CJFWindowDragVCDelegate <NSDraggingDestination>

@required
-(NSArray<NSString *> *)getRegisterForDraggedTypes;

@end

#endif /* CJFViewControllerProtocol_h */
