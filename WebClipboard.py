import requests
import json
import win32clipboard
import threading


def new_thread(func):
    def wrapper(*args, **kwargs):
        th = threading.Thread(
            target=func, args=args)
        th.setDaemon(True)
        th.start()
    return wrapper


class WebClipboard():
    def __init__(self):
        self.server_url = "http://119.29.130.26:7000/webclipboard/"
        self.auth_admin = "iiioooppp"
        self.webClip_contents = []
        self.locClip_content = ""

    @new_thread
    def read_web_clip(self, start, end, call=None):
        '''
        读取web的内容
        将返回内容传给回调函数
        内容的顺序是新的在前,旧的在后
        当start end 都为 0 时 返回所有内容
        '''
        data = {"auth": self.auth_admin, "start": start, "end": end}
        r = requests.post(self.server_url+"read", json=data)
        json_all = json.loads(r.text)
        if json_all.get("sucess") and json_all.get("contents", None) != None:
            self.webClip_contents = json_all.get("contents")
            call(json_all)
        else:
            call(json_all)

    @new_thread
    def write_web_clip(self, content: str, call=None):
        data = {"auth": self.auth_admin, "content": content}
        r = requests.post(self.server_url+"write", json=data)
        json_all = json.loads(r.text)
        if json_all.get("sucess"):
            self.webClip_contents.insert(0, content)
        call(json_all)

    @new_thread
    def delete_web_clip(self, index: int, call=None):
        data = {"auth": self.auth_admin, "index": index}
        r = requests.post(self.server_url+"delete", json=data)
        json_all = json.loads(r.text)
        if json_all.get("sucess") and json_all.get("index") == index:
            self.webClip_contents.pop(index)
            call(json_all)


def read_local_clip():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            content = win32clipboard.GetClipboardData(
                win32clipboard.CF_UNICODETEXT)
            return content
        else:
            return False
    finally:
        win32clipboard.CloseClipboard()


def write_local_clip(content: str):
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.SetClipboardData(
            win32clipboard.CF_UNICODETEXT, content)
        return True
    finally:
        win32clipboard.CloseClipboard()
