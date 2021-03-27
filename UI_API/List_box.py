from threading import Lock, Thread
from tkinter import Listbox
from Search_for_suggestions import Search_for_suggestions
from WebClipboard import WebClipboard, read_local_clip, write_local_clip
from State import State_show


class List_box():
    def __init__(self, list_box: Listbox):
        self.list_box = list_box
        self.mediator = object
        self.state = object
        self.th_lock = False
        self.pre_selection = None
        self.webClip_continuance = True
        self.suggestion = Search_for_suggestions()
        self.webClipboard = WebClipboard()
        self.update_webclip()

    def update_list_box(self, content: list):
        self.list_box.delete(0, 'end')
        for i in content:
            self.list_box.insert('end', i)

    def update_suggestions_(self, query: str):
        # self.th_lock.acquire()
        self.th_lock = True
        self.update_list_box(self.suggestion.get_suggestions(query))
        # self.th_lock.release()
        self.th_lock = False

    def update_suggestions(self, query: str):
        if not self.th_lock:
            th = Thread(target=self.update_suggestions_, args=(query,))
            th.start()
        return True

    def update_webclip(self):
        if not self.th_lock and self.state == "show":
            print("update_webclip")
            content = self.webClipboard.read_web_clip()
            content.insert(0, read_local_clip())
            self.update_list_box(content)

    def update_webclip_continuance(self):
        pass

    def get_focues(self):
        if str(self.list_box.focus_get()) != ".!listbox" and self.get_size() != 0:
            print("get_focues")
            self.list_box.focus_set()
            self.list_box.selection_set(0)

    def get_curselection(self):
        # (0,)
        return self.list_box.curselection()

    def get_size(self):
        return self.list_box.size()

    def selection_includes(self, index):
        return self.list_box.selection_includes(index)
