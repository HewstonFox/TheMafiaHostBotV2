from typing import TypedDict, Any, List, Union, Optional


class MessageMenuButtonOption(TypedDict):
    name: str
    value: Any


class _MessageMenuButtonBase(TypedDict):
    type: str


class MessageMenuButton(_MessageMenuButtonBase, total=False):
    name: str
    description: str
    key: str
    min: Union[int, float, None]
    max: Union[int, float, None]
    options: List[MessageMenuButtonOption]
    buttons: List['MessageMenuButton']
    disable_special_buttons: Optional[bool]


class MessageMenu(TypedDict, total=False):
    description: str
    buttons: List[MessageMenuButton]
    disable_special_buttons: Optional[bool]


class ButtonType:
    route = 'route'
    select = 'select'
    toggle = 'toggle'
    int = 'int'
    float = 'float'
    decimal = 'decimal'
    endpoint = 'endpoint'
