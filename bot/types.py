import asyncio
import inspect
from typing import Union, TypedDict, Callable

from aiogram.types import LoginUrl, CallbackGame, User

ChatId = Union[int, str]


class MarkupKeyboardDict(TypedDict):
    text: str
    url: str
    login_url: LoginUrl
    callback_data: str
    switch_inline_query: str
    switch_inline_query_current_chat: str
    callback_game: CallbackGame
    pay: bool


class Proxy(dict):
    def __init__(self, seq=None, **kwargs):
        super(Proxy, self).__init__(seq, **kwargs)
        self.__subscribers = []

    def subscribe(self, *subscribers: Callable[[dict], any]):
        self.__subscribers.extend(subscribers)

    def unsubscribe(self, *subscribers: Callable[[dict], any]):
        for subscriber in self.__subscribers[:]:
            if subscriber in subscribers:
                self.__subscribers.remove(subscriber)

    def __ping_subscribers(self):
        for subscriber in self.__subscribers:
            if inspect.iscoroutinefunction(subscriber):
                asyncio.create_task(subscriber(self))
            else:
                subscriber(self)

    def __setitem__(self, key, value):
        super(Proxy, self).__setitem__(key, value)
        self.__ping_subscribers()

    def __delitem__(self, key):
        super(Proxy, self).__delitem__(key)
        self.__ping_subscribers()

    def pop(self, key):
        super(Proxy, self).pop(key)
        self.__ping_subscribers()


class RoleMeta:
    index: int
    user: User
    won: bool
    alive: bool
    shortcut: str


class ResultConfig(TypedDict):
    alive: list[RoleMeta]
    dead: list[RoleMeta]
    winners: list[RoleMeta]
    losers: list[RoleMeta]
    alive_roles: dict[str, int]
