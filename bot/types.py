from typing import Union, TypedDict

from aiogram.types import LoginUrl, CallbackGame

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
