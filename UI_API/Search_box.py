import webbrowser
from Search_engine import search_engine
from tkinter import Entry
from time import sleep


class Search_box():
    def __init__(self, entry: Entry):
        self.entry = entry
        self.entry.configure(validatecommand=self.validatecommand)
        self.mediator = object
        self.state = object

    def validatecommand(self):
        self.mediator.notify(self, {"suggestions": True})
        return True

    def get_focues(self):
        if str(self.entry.focus_get()) != ".!entry":
            self.entry.focus_set()

    def search_web(self):
        if search_engine.search_engines[0].get("name") == "google翻译":
            self.mediator.notify(self, {"translation_query": self.entry.get()})
        else:
            webbrowser.open(search_engine.search_engines[0].get("url").format(
                self.entry.get()))
            self.entry.delete(0, 'end')

    def get_content(self):
        return self.entry.get()
