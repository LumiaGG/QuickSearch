from tkinter import Tk
import win32com.client
from win32gui import FindWindow, SetForegroundWindow
from Logger import logger
shell = win32com.client.Dispatch("WScript.Shell")


class Base_window():
    def __init__(self, main_window: Tk):
        self.main_window = main_window
        self.is_setup = True
        self.hwnd = None
        self.state = object

    def show_window(self):
        self.main_window.deiconify()
        self.main_window.update()
        if self.is_setup:
            self.is_setup = False
            self.hwnd = FindWindow(None, 'search')
        try:
            shell.SendKeys('%')
            SetForegroundWindow(self.hwnd)
        except:
            logger.warning("Base_window show_window SetForegroundWindow")

    def hide_window(self):
        self.main_window.withdraw()
        self.main_window.update()
