from tkinter import Label
from Search_engine import search_engine


class Side_label():
    def __init__(self, label_logos: list):
        self.label_logos = label_logos
        self.mediator = object
        self.state = object
        search_engine.load_img()
        self.update_logo()
        self.bind_click()

    def update_logo(self):
        for i, label in enumerate(self.label_logos):
            if i == 0:
                label.config(
                    image=search_engine.search_engines[i].get("logo_big"))
            else:
                label.config(image=search_engine.search_engines[i].get("logo"))

    def update_logo_click(self, e, index):
        for i in range(index):
            search_engine.swap_search_engin()
        self.update_logo()

    def bind_click(self):
        for i, logo in enumerate(self.label_logos):
            logo.bind('<1>', handlerAdaptor(self.update_logo_click, i))


def handlerAdaptor(fun, index):
    return lambda event, fun=fun, index=index: fun(event, index)
