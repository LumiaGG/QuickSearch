import requests
import json
import win32clipboard
import threading


class WebClipboard():
    def __init__(self):
        self.server_host = None
        self.server_port = None

    def read_web_clip(self):
        return ["1", "2", "3"]

    def write_web_clip(self, content: str):
        pass


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
