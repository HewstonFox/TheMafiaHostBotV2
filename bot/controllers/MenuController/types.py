from typing import TypedDict, Any, List


class MessageMenuButtonOption(TypedDict):
    name: str
    value: Any


class _MessageMenuButtonBase(TypedDict):
    type: str


class MessageMenuButton(_MessageMenuButtonBase, total=False):
    name: str
    description: str
    key: str
    options: List[MessageMenuButtonOption]
    buttons: List['MessageMenuButton']


class MessageMenu(TypedDict):
    description: str
    buttons: List[MessageMenuButton]


class ButtonType:
    route = 'route'
    select = 'select'
    toggle = 'toggle'
    int = 'int'
    float = 'float'
    decimal = 'decimal'
