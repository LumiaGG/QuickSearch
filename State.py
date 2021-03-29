from Search_engine import search_engine


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

    def update_UI_state(self):
        print("update_UI_state")
        self.context.list_box.state = self.context.state.statement()
        self.context.side_label.state = self.context.state.statement()
        self.context.search_box.state = self.context.state.statement()
        self.context.base_window.state = self.context.state.statement()
        self.context.text_view.state = self.context.state.statement()


class State_show(State):

    def statement(self):
        return "show"

    def win_q(self,):
        print("关")
        self.context.control.unhook_suppress()
        self.context.state = State_hide(self.context)
        self.update_UI_state()
        self.context.base_window.hide_window()

    def win_w(self,):
        print("win_w")
        from WebClipboard import read_local_clip
        self.context.text_view.show_view()
        self.context.text_view.write_view(read_local_clip())

    def tab(self,):
        print("tab")
        search_engine.swap_search_engin()
        self.context.side_label.update_logo()

    def enter(self):
        print('enter')
        if self.context.list_box.focues():
            print("list_box")
            self.context.list_box.enter()
        elif self.context.search_box.focues():
            print("search_box")
            self.context.search_box.enter()
            if search_engine.search_engines[0].get("name") != "google翻译":
                self.win_q()

    def up(self):
        print("up")
        if (self.context.list_box.selection_includes(0)):
            self.context.search_box.get_focues()

    def down(self):
        print("down")
        print(self.context.list_box.get_size())
        self.context.list_box.get_focues()


class State_hide(State):

    def statement(self):
        return "hide"

    def win_q(self,):
        print("开")
        self.context.control.hook_suppress()
        self.context.state = State_show(self.context)
        self.update_UI_state()
        self.context.base_window.show_window()
        self.context.search_box.get_focues()
        if self.context.search_box.get_content() == "":
            self.context.list_box.update_webclip()

    def win_w(self,):
        print("现在是hide状态,执行了win_w")
        self.context.control.hook_tab()
        self.context.state = State_show(self.context)
        self.update_UI_state()
        self.context.base_window.show_window()
        self.context.text_view.show_view()
        from WebClipboard import read_local_clip
        self.context.text_view.write_view(read_local_clip())
