from Search_engine import search_engine
from MyEnum import WindowsShowMode
from Logger import logger


class State():

    def __init__(self, context):
        self.context = context

    def __context(self,):
        return self.context

    def statement(self,):
        pass

    def win_q(self):
        pass

    def win_w(self):
        pass

    def tab(self):
        pass

    def enter(self):
        pass

    def down(self):
        pass

    def up(self):
        pass

    def left(self):
        pass

    def update_UI_state(self):
        logger.info("update_UI_state")
        self.context.list_box.state = self.context.state.statement()
        self.context.side_label.state = self.context.state.statement()
        self.context.search_box.state = self.context.state.statement()
        self.context.base_window.state = self.context.state.statement()
        self.context.text_view.state = self.context.state.statement()


class State_show(State):

    def statement(self):
        return WindowsShowMode.show

    def win_q(self,):
        logger.info("hide")
        self.context.control.unhook_suppress()
        self.context.state = State_hide(self.context)
        self.update_UI_state()
        self.context.base_window.hide_window()

    def win_w(self,):
        logger.info("win_w")
        from WebClipboard import read_local_clip
        self.context.text_view.show_view()
        self.context.text_view.write_view(read_local_clip())

    def tab(self,):
        logger.info("tab")
        search_engine.swap_search_engin()
        self.context.side_label.update_logo()

    def enter(self):
        logger.info('enter')
        if self.context.list_box.focues():
            logger.info("focues list_box")
            self.context.list_box.enter()
        elif self.context.search_box.focues():
            logger.info("focues search_box")
            self.context.search_box.enter()
            if search_engine.search_engines[0].get("name") != "google翻译":
                self.win_q()

    def up(self):
        logger.info("up")
        if (self.context.list_box.selection_includes(0)):
            self.context.search_box.get_focues()

    def down(self):
        logger.info("down")
        self.context.list_box.get_focues()

    def left(self):
        logger.info("left")
        self.context.list_box.left()


class State_hide(State):

    def statement(self):
        return WindowsShowMode.hide

    def win_q(self,):
        logger.info("show")
        self.context.control.hook_suppress()
        self.context.state = State_show(self.context)
        self.update_UI_state()
        self.context.base_window.show_window()
        self.context.search_box.get_focues()
        if self.context.search_box.get_content() == "":
            self.context.list_box.update_webclip()

    def win_w(self,):
        logger.info("win_w")
        self.context.control.hook_suppress()
        self.context.state = State_show(self.context)
        self.update_UI_state()
        self.context.base_window.show_window()
        self.context.text_view.show_view()
        from WebClipboard import read_local_clip
        self.context.text_view.write_view(read_local_clip())
