from tkinter import Text
from tkinter.constants import W
import tkinter.font as tkFont
from threading import Thread
from Translation import Translation
from MyEnum import WindowsShowMode


class Text_view():
    def __init__(self, Text_view: Text):
        self.text_view = Text_view
        self.mediator = object
        self.state = WindowsShowMode.hide
        self.isShow = False
        self.translation = Translation()
        self.ft = tkFont.Font(family='微软雅黑', size=11,)

    def show_view(self):
        if not self.isShow:
            self.isShow = True
            self.text_view.place(x=40, y=55)

    def hide_view(self):
        if self.isShow:
            self.isShow = False
            self.text_view.place_forget()

    def write_view(self, query):
        def get_max_word_len():
            max_word_len = 0
            for i in range(1, len(ret)):
                for j in range(1, len(ret[i])):
                    if len(ret[i][j][0]) > max_word_len:
                        max_word_len = len(ret[i][j][0])
            return max_word_len

        def parse_ret(row):
            space = max_word_len+3 - \
                len(row[0]) if len(row[0]) < 15 else 0
            content = f'  {row[0]}{space*" "}{row[1]}\n'
            return content

        ret = self.translation.translat(query)
        max_word_len = get_max_word_len()

        self.text_view.delete("1.0", "end")

        if ret[0] != -1:
            if ret[0] == 0:  # 单词
                count = 1
                for i in range(1, len(ret)):
                    self.text_view.insert(
                        f"{count}.0", f'词性:{ret[i][0]}\n')  # 插入词性
                    for j in range(1, len(ret[i])):  # 遍历该词性下的所有解释
                        count += 1
                        self.text_view.insert(
                            f"{count}.0", parse_ret(ret[i][j]))
                    count += 1

        if ret[0] == 1:
            self.text_view.insert(
                f"1.0", f'拼音:{ret[1][0]}\n-----------\n')  # 插入拼音
            count = 3
            for i in range(1, len(ret[1])):
                self.text_view.insert(
                    f"{count}.0", f'  {ret[1][i]}\n-----------\n')  # 插入句子
