import sys  # NOQA: E402

sys.path.append("..")  # NOQA: E402
import tkinter.font as tkFont
from tkinter import *

from Search_engine import search_engine


class MyUI():
    def __init__(self, main_window: Tk):
        self.main_window = main_window
        self.constructing()

    def constructing(self):
        # base_window

        self.main_window.title('search')
        self.main_window.overrideredirect(True)
        self.main_window.geometry("600x350+400+250")
        self.main_window.attributes("-topmost", -1)
        self.main_window.attributes("-alpha", 0.9)

        bg = Label(self.main_window, width='500',
                   height='220', bg='#F5F5F5').pack()
        # /base_window

        # side_label
        self.lable_logo_list = []
        for i in range(search_engine.search_engines_num):
            self.lable_logo_list.append(Label(
                self.main_window, bg='#F5F5F5'))
        for i, label in enumerate(self.lable_logo_list):
            if i == 0:
                label.place(x=3, y=7)
            else:
                label.place(x=3, y=17 + 40 * i)
        # /side_label

        # search_box
        self.font = tkFont.Font(
            family='Fixdsys', size=18, weight=tkFont.BOLD)
        self.entry = Entry(self.main_window, font=self.font,
                           fg='SteelBlue', bg='#F5F5F5', width='40', validate='key',)
        self.entry.place(x=46, y=15)
        # /search_box

        # list_box
        self.list_box = Listbox(self.main_window, takefocus=0, width=41, height=11, bg='#F5F5F5',
                                font=self.font, fg='SteelBlue', selectbackground='SteelBlue', borderwidth=0)
        self.list_box.place(x=40, y=55)
        # /list_box

        # Text_view
        self.text_view = Text(self.main_window, width=76,
                              height=21, bg='#F5F5F5')
        self.text_view.place(x=40, y=55)
        self.text_view.place_forget()

        # /Text_view
