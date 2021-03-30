from enum import Enum


class NotifyEvent(Enum):
    validatecommand = 0
    translation = 1
    insert_history = 2
    type_content = 3  # 将listbox的内容放到entry中


class ContentShowMode(Enum):
    none = 0
    clip = 1
    history = 2
    translation = 3


class WindowsShowMode(Enum):
    show = 0
    hide = 1
