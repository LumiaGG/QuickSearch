from UI_API.Search_box import Search_box
from UI_API.List_box import List_box
from UI_API.Text_view import Text_view
from time import sleep
from WebClipboard import new_thread
from MyEnum import NotifyEvent


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
        if event.get(NotifyEvent.validatecommand, None):
            self.request_suggestions()
        elif event.get(NotifyEvent.translation, None):
            self.text_view.show_view()
            self.text_view.write_view(event.get(NotifyEvent.translation))
        elif event.get(NotifyEvent.type_content, None):
            self.search_box.entry.delete(0, 'end')
            self.search_box.entry.insert(
                0, event.get(NotifyEvent.type_content))
            self.search_box.get_focues()
        elif event.get(NotifyEvent.insert_history, None):
            self.list_box.history.insert(
                event.get(NotifyEvent.insert_history))
        else:
            pass

    @new_thread
    def request_suggestions(self):
        # 延时获取entry里面的内容,因为validate回调执行的时候,不能获得最新的内容
        # 直接在此函数加载 suggestions
        self.text_view.hide_view()
        sleep(0.001)
        print(self.search_box.entry.get())
        if self.search_box.entry.get() == "":  # 检查内容有效性
            # 显示 webclip
            self.list_box.update_webclip()
        elif self.search_box.entry.get() == " ":
            # 显示 搜索历史
            self.list_box.update_history()
        else:
            pass
