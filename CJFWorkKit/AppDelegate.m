//
//  AppDelegate.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 16/4/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "AppDelegate.h"
#import "CJFTimerManager.h"
#import "CJFInitManager.h"
#import "CJFWindowController.h"

@interface AppDelegate ()

@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    // Insert code here to initialize your application
    [[CJFInitManager sharedManager] InitEnvironment];
    removeFileWitName(@"test");
    //在线调试请注释此行代码
#ifndef TEST_CJFWORKKIT_DEBUG
    redirectNSlogToDocumentFolder(@"Setting/runLog");
#endif
    
    [CJFTimerManager sharedManager];
}

- (void)applicationWillTerminate:(NSNotification *)aNotification {
    // Insert code here to tear down your application
}

- (BOOL)applicationShouldHandleReopen:(NSApplication *)sender hasVisibleWindows:(BOOL)flag
{
    static NSWindowController* mywc = nil;
    if( !flag ){
        NSStoryboard *mainSB = [NSStoryboard storyboardWithName:@"Main" bundle:[NSBundle mainBundle]];
        mywc = [mainSB instantiateInitialController];
        [mywc showWindow:self];
    }
    return NO;
}

//- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender
//{
//    return YES;
//}

- (void)applicationWillBecomeActive:(NSNotification *)notification
{
    
}

@end
