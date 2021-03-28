from State import State_show
from tkinter import Tk
from UI_API.MyUI import MyUI
from UI_API.Base_window import Base_window
from UI_API.List_box import List_box
from UI_API.Search_box import Search_box
from UI_API.Side_label import Side_label
from UI_API.Text_view import Text_view
from Mediator import Search_Mediator
from Control import MyKeyboard


class Launcher():
    def __init__(self):
        self.main_window = Tk()
        self.ui = MyUI(self.main_window)
        self.base_window = Base_window(self.main_window)
        self.side_label = Side_label(self.ui.lable_logo_list)
        self.search_box = Search_box(self.ui.entry)
        self.list_box = List_box(self.ui.list_box)
        self.text_view = Text_view(self.ui.text_view)
        Search_Mediator(self.search_box, self.list_box, self.text_view)

        self.state = State_show(self)
        self.control = MyKeyboard(self)
        self.main_window.mainloop()


launcher = Launcher()
