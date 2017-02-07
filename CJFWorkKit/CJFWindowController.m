//
//  CJFWindowController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/9/12.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "CJFWindowController.h"
#import "CJFWindowManager.h"

@interface CJFWindowController ()<NSWindowDelegate,NSDraggingDestination>

@end

@implementation CJFWindowController

- (void)windowDidLoad {
    [super windowDidLoad];
    self.window.delegate = self;
    
    // Implement this method to handle any initialization after your window controller's window has been loaded from its nib file.
}

+(CJFWindowController*)showNewWindowWithControllerName:(NSString*)name
{
    if( !validateString(name) ){
        return nil;
    }
    
    NSStoryboard* storyboard = [NSStoryboard storyboardWithName:@"Main" bundle:[NSBundle mainBundle]];
    NSViewController* vc = [storyboard instantiateControllerWithIdentifier:name];
    
    if( vc == nil ){
        return nil;
    }
    
    
    CJFWindowController* newWindowVC = [[CJFWindowController alloc] initWithWindowNibName:@"CJFWindowController"];
    newWindowVC.contentViewController = vc;
    newWindowVC.functionName = name;
    
    if( [vc conformsToProtocol:NSProtocolFromString(@"CJFWindowDragVCDelegate")] ){
        id<CJFWindowDragVCDelegate> dargVC = (id<CJFWindowDragVCDelegate>)vc;
        NSArray<NSString*>* dragList = [dargVC getRegisterForDraggedTypes];
        if( validateArray(dragList) ){
            [newWindowVC.window registerForDraggedTypes:dragList];
        }
    }
    
    return newWindowVC;
}

- (void)windowWillClose:(NSNotification *)notification
{
    [[CJFWindowManager sharedManager] closeWindowWithNotifaction:self.functionName];
}

#pragma mark - 拖拽相关操作

- (NSDragOperation)draggingEntered:(id <NSDraggingInfo>)sender{
    if( [self.contentViewController conformsToProtocol:NSProtocolFromString(@"CJFWindowDragVCDelegate")] ){
        if( [self.contentViewController respondsToSelector:@selector(draggingEntered:)] ){
            id<CJFWindowDragVCDelegate> dargVC = (id<CJFWindowDragVCDelegate>)self.contentViewController;
            return [dargVC draggingEntered:sender];
        }
        return NSDragOperationNone;
    }else{
        return NSDragOperationNone;
    }
}

- (NSDragOperation)draggingUpdated:(id <NSDraggingInfo>)sender
{
    if( [self.contentViewController conformsToProtocol:NSProtocolFromString(@"CJFWindowDragVCDelegate")] ){
        if( [self.contentViewController respondsToSelector:@selector(draggingUpdated:)] ){
            id<CJFWindowDragVCDelegate> dargVC = (id<CJFWindowDragVCDelegate>)self.contentViewController;
            return [dargVC draggingUpdated:sender];
        }else if ( [self.contentViewController respondsToSelector:@selector(draggingEntered:)]  ){
            id<CJFWindowDragVCDelegate> dargVC = (id<CJFWindowDragVCDelegate>)self.contentViewController;
            return [dargVC draggingEntered:sender];
        }else{
            return NSDragOperationNone;
        }
    }else{
        return NSDragOperationNone;
    }
}

- (void)draggingExited:(id<NSDraggingInfo>)sender{
    if( [self.contentViewController conformsToProtocol:NSProtocolFromString(@"CJFWindowDragVCDelegate")] ){
        if( [self.contentViewController respondsToSelector:@selector(draggingExited:)] ){
            id<CJFWindowDragVCDelegate> dargVC = (id<CJFWindowDragVCDelegate>)self.contentViewController;
            [dargVC draggingExited:sender];
        }
    }
}

- (BOOL)performDragOperation:(id <NSDraggingInfo>)sender
{
    if( [self.contentViewController conformsToProtocol:NSProtocolFromString(@"CJFWindowDragVCDelegate")] ){
        if( [self.contentViewController respondsToSelector:@selector(performDragOperation:)] ){
            id<CJFWindowDragVCDelegate> dargVC = (id<CJFWindowDragVCDelegate>)self.contentViewController;
            return [dargVC performDragOperation:sender];
        }
        return NO;
    }else{
        return NO;
    }
}

@end
