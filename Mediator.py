from UI_API.Search_box import Search_box
from UI_API.List_box import List_box
from UI_API.Text_view import Text_view
import threading
from time import sleep


class Mediator():
    def notify(self, sender: object, event: str) -> None:
        pass


class Search_Mediator(Mediator):
    def __init__(self, search_box: Search_box, list_box: List_box, text_view: Text_view) -> None:
        self.search_box = search_box
        self.search_box.mediator = self
        self.list_box = list_box
        self.list_box.mediator = self
        self.text_view = text_view
        self.text_view.mediator = self

    def notify(self, sender: object, event: dict) -> None:
        if event.get("suggestions", None):
            if not self.list_box.th_lock:  # 检查锁
                th = threading.Thread(target=self.request_suggestions)
                th.start()
        elif event.get("translation_query", None):
            self.text_view.show_view()
            self.text_view.write_view(event.get("translation_query"))
        elif event.get("type_sug", None):
            self.search_box.entry.delete(0, 'end')
            self.search_box.entry.insert(0, event.get("type_sug"))
            self.search_box.get_focues()
        else:
            pass

    def request_suggestions(self):
        # 延时获取entry里面的内容,因为validate回调执行的时候,不能获得最新的内容
        # 直接在此函数加载 suggestions
        self.text_view.hide_view()
        sleep(0.1)
        if self.search_box.entry.get() == "":  # 检查内容有效性
            self.list_box.update_webclip()
        else:
            self.list_box.update_suggestions_(self.search_box.entry.get())
