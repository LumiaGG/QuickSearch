import keyboard
import State
import Clipboard


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
        hotkeys = self.enmu_hotkey()
        for hotkey in hotkeys:
            self.keyboard.remove_hotkey(hotkey[0])
            self.keyboard.add_hotkey(hotkey[0], self.act_hotkey, hotkey)
