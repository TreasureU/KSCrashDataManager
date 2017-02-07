//
//  QuicklyImportViewController.m
//  CJFWorkKit
//
//  Created by ChengJianFeng on 2016/11/28.
//  Copyright © 2016年 ChengJianFeng. All rights reserved.
//

#import "QuicklyImportViewController.h"

@interface QuicklyImportViewController ()

@property(nonatomic,strong) NSString* filePath;

@end

@implementation QuicklyImportViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do view setup here.
    [self resetState];
}

-(void)resetState
{
    self.filePath = nil;
    self.tipLabel.stringValue = @"请将文件拖入这个窗口的任意位置，然后松开鼠标......\n拖入文件后，请填写build、version和简短描述、设备类型，最后点击导入，会自动为文件生成[xxxiPhone/xxipad]_[version]_[build]_[简短描述]，如果导入时命名冲突，那么会导致导入失败，请更正命名后重新导入。如果决定文件过多，可以点击打开目录，删除部分文件，但请不要直接自己对文件做拖入操作，确保命名符合规范，以免日后脚本不兼容。";
    self.buildTF.stringValue = @"";
    self.versionTF.stringValue = @"";
    self.appendDesTF.stringValue = @"";
}

-(NSArray<NSString *> *)getRegisterForDraggedTypes
{
    return @[NSColorPboardType, NSFilenamesPboardType];
}

- (NSDragOperation)draggingEntered:(id <NSDraggingInfo>)sender{
    
    NSPasteboard *pboard;
    NSDragOperation sourceDragMask;
    
    sourceDragMask = [sender draggingSourceOperationMask];
    pboard = [sender draggingPasteboard];
    
    if ( [[pboard types] containsObject:NSColorPboardType] ) {
        if (sourceDragMask & NSDragOperationGeneric) {
            return NSDragOperationGeneric;
        }
    }
    if ( [[pboard types] containsObject:NSFilenamesPboardType] ) {
        if (sourceDragMask & NSDragOperationLink) {
            return NSDragOperationLink;
        } else if (sourceDragMask & NSDragOperationCopy) {
            return NSDragOperationCopy;
        }
    }
    return NSDragOperationNone;
}

- (void)draggingExited:(id<NSDraggingInfo>)sender{
    
}

- (BOOL)performDragOperation:(id <NSDraggingInfo>)sender
{
    NSPasteboard *pboard = [sender draggingPasteboard];
    
    if([[pboard types] containsObject:NSFilenamesPboardType]){
        NSArray *files = [pboard propertyListForType:NSFilenamesPboardType];
        for(NSString *filePath in files){
            if([filePath.pathExtension isEqualToString:@""]){
                self.filePath = filePath;
                self.tipLabel.stringValue = [NSString stringWithFormat:@"导入文件的位置是：%@\n",self.filePath];
                return YES;
            }
        }
    }
    
    return NO;
}

- (IBAction)deviceBtnClick:(NSPopUpButton *)sender {
}

- (IBAction)importBtnClick:(NSButton *)sender {
    NSString* deviceName = self.appNameBtn.selectedItem.title;
    NSString* build = self.buildTF.stringValue;
    NSString* version = self.versionTF.stringValue;
    NSString* appendName = self.appendDesTF.stringValue;
    if( validateString(deviceName) && validateString(build) && validateString(version) && validateString(appendName) && validateString(self.filePath)){
        NSString* sourcePath = nil;
        if( [deviceName isEqualToString:@"iPad"] ){
            deviceName = @"xxipad";
            sourcePath = getFilePath(@"SourceSymbol/self");
        }else{
            deviceName = @"xxxiPhone";
            sourcePath = getFilePath(@"SourceSymbol/self");
        }
        NSString* fileName = [NSString stringWithFormat:@"%@_%@_%@_%@",deviceName,version,build,appendName];
        NSString* filePath = [sourcePath stringByAppendingPathComponent:fileName];
        if( [[NSFileManager defaultManager] fileExistsAtPath:filePath] ){
            [self willAppendLog:[NSString stringWithFormat:@"%@ 文件名已存在，请修改简短描述\n",fileName]];
        }else{
            NSString* cmd = [NSString stringWithFormat:@"cp %@ %@",self.filePath,filePath];
            runSystemCommand(cmd, getMainDocumentDirPath());
            [self willAppendLog:@"文件导入成功\n"];
        }
    }else{
        [self willAppendLog:@"参数未填写完全，请继续填写。\n"];
    }
}

- (IBAction)resetBtnClick:(NSButton *)sender {
    [self resetState];
}

- (IBAction)openDirBtnClick:(NSButton *)sender {
    NSString* sourcePath = nil;
    NSString* deviceName = self.appNameBtn.selectedItem.title;
    if( [deviceName isEqualToString:@"iPad"] ){
        sourcePath = getFilePath(@"SourceSymbol/self");
    }else{
        sourcePath = getFilePath(@"SourceSymbol/self");
    }
    if( validateString(sourcePath) ){
        NSString* result = runSystemCommand([NSString stringWithFormat:@"open %@",sourcePath], getMainDocumentDirPath());
        [self willAppendLog:result];
    }else{
        [self willAppendLog:@"打开目录失败：目录未选择"];
    }
}

#pragma mark - 私有方法
-(void)willAppendLog:( NSString*)appendStr
{
    if( validateString(appendStr) ){
        self.tipLabel.stringValue = [self.tipLabel.stringValue stringByAppendingString:[appendStr stringByAppendingString:@"\n"]];
    }
}


@end
