import keyboard
import State
import Clipboard
'''
休眠后, add_hotkey 将不可用
使用 hook_key 代替
'''


class MyKeyboard():
    def __init__(self, context):
        self.keys = [["left windows", False], ['q', False], [
            'w', False], ['tab', True], ['down', False], ['up', False], ['left', False], ['enter', False]]
        self.key_map = {}
        self.context = context
        self.keyboard = keyboard
        self.init_hook()

    def init_hook(self):
        for i, k in enumerate(self.keys):
            self.keyboard.hook_key(k[0], self.call_key, k[1])

    def unhook_suppress(self):
        '''
        释放被suppress的key
        '''
        for i, k in enumerate(self.keys):
            if k[1] == True:
                self.keyboard.unhook_key(k[0])

    def hook_suppress(self):
        '''
        hook 需要 suppress 的key
        '''
        for i, k in enumerate(self.keys):
            if k[1] == True:
                self.keyboard.hook_key(k[0], self.call_key, True)

    def call_key(self, e):
        self.key_map[e.name] = e.event_type
        for i, hk in enumerate(self.enmu_hotkey()):
            if len(hk) == 3:
                if self.key_map.get(hk[0]) == "down" and self.key_map.get(hk[1]) == "down":
                    hk[2]()
            elif len(hk) == 2:
                if self.key_map.get(hk[0]) == "down":
                    hk[1]()

    def enmu_hotkey(self,):
        hotkeys = [("left windows", "q",  self.context.state.win_q),
                   ("left windows", "w", self.context.state.win_w),
                   ("down", self.context.state.down),
                   ("up", self.context.state.up),
                   ("left", self.context.state.left),
                   ("tab", self.context.state.tab),
                   ("enter", self.context.state.enter),
                   ]
        return hotkeys


class Control():

    def __init__(self, context):
        self.context = context
        self.keyboard = keyboard

        hotkeys = self.enmu_hotkey()
        for hotkey in hotkeys:
            self.keyboard.add_hotkey(hotkey[0], self.act_hotkey, hotkey)
        keyboard.hook_key("tab", self.callback_tab, suppress=True)

    def callback_tab(self, e):
        if e.event_type == 'down':
            self.context.state.tab()

    def hook_tab(self):
        keyboard.hook_key("tab", self.callback_tab, suppress=True)

    def unhook_tab(self):
        keyboard.unhook("tab")

    def act_hotkey(self, name, act):
        act()
        self.update_hotkey()

    def enmu_hotkey(self,):
        hotkeys = [('windows+q', self.context.state.win_q,),
                   ('windows+w', self.context.state.win_w,),
                   ('enter', self.context.state.enter,),
                   ('down', self.context.state.down),
                   ('up', self.context.state.up)
                   ]
        return hotkeys

    def update_hotkey(self,):
        self.keyboard.hook(print)
        hotkeys = self.enmu_hotkey()
        for hotkey in hotkeys:
            self.keyboard.remove_hotkey(hotkey[0])
            self.keyboard.add_hotkey(hotkey[0], self.act_hotkey, hotkey)
