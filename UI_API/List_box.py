from ctypes import wintypes
from History import History
from tkinter import Listbox, constants
from Search_for_suggestions import Search_for_suggestions
from WebClipboard import WebClipboard, read_local_clip, write_local_clip
from History import History
from MyEnum import ContentShowMode, WindowsShowMode
from Logger import logger


class List_box():
    def __init__(self, list_box: Listbox):
        self.list_box = list_box
        self.mediator = object
        self.state = WindowsShowMode.show
        self.pre_selection = None
        self.show_mode = ContentShowMode.clip
        self.clip_contents = []
        self.webClipboard = WebClipboard()
        self.history = History()
        self.update_webclip()

    def update_list_box(self, content: list):
        self.list_box.delete(0, 'end')
        for i in content:
            self.list_box.insert('end', i)

    def update_webclip(self):
        if self.state == WindowsShowMode.show:
            logger.info("update_webclip")
            self.show_mode = ContentShowMode.clip
            self.webClipboard.locClip_content = read_local_clip()
            self.webClipboard.read_web_clip(0, 0, self.webclip_call)

    def webclip_call(self, json_all):
        '''
        请求webclip后的回调
        '''
        if self.show_mode == ContentShowMode.clip:
            contents = self.webClipboard.webClip_contents.copy()
            contents.insert(0, self.webClipboard.locClip_content)
            self.update_list_box(contents)

    def update_history(self):
        if self.state == WindowsShowMode.show:
            logger.info("update_history")
            self.show_mode = ContentShowMode.history
            self.update_list_box(self.history.get())

    def get_focues(self):
        if str(self.list_box.focus_get()) != ".!listbox" and self.get_size() != 0:
            self.list_box.focus_set()
            self.list_box.selection_set(0)

    def get_curselection(self):
        # (0,)
        return self.list_box.curselection()

    def get_size(self):
        return self.list_box.size()

    def selection_includes(self, index):
        return self.list_box.selection_includes(index)

    def focues(self):
        if str(self.list_box.focus_get()) == ".!listbox":
            return True
        else:
            return False

    def enter(self):
        if self.show_mode == ContentShowMode.clip:
            if self.get_curselection()[0] == 0:
                # 上传
                logger.info("上传剪切板")
                self.webClipboard.write_web_clip(
                    self.webClipboard.locClip_content, self.webclip_call)
            else:
                # 下载
                logger.info("下载剪切板")
                write_local_clip(
                    self.webClipboard.webClip_contents[self.get_curselection()[
                        0]-1])

                self.webClipboard.locClip_content = read_local_clip()
                contents = self.webClipboard.webClip_contents.copy()
                contents.insert(0, self.webClipboard.locClip_content)
                self.update_list_box(contents)
        else:
            sug = self.list_box.get(self.get_curselection()[0])
            self.mediator.notify(self, {"type_sug": sug})

    def left(self):
        '''
        注意self.get_curselection()[0] == 0 是本地内容
        '''
        if self.show_mode == ContentShowMode.clip:
            logger.info("删除剪切板")
            if self.get_curselection() != () and self.get_curselection()[0] > 0:
                self.webClipboard.delete_web_clip(
                    self.get_curselection()[0]-1, self.webclip_call)

        elif self.show_mode == ContentShowMode.history:
            if self.get_curselection() != ():
                self.history.pop(self.get_curselection()[0])
                self.update_history()
