from typing import List, Tuple, Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.types import MarkupKeyboardDict


def arr2keyword_markup(buttons: List[List[MarkupKeyboardDict]]):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(**btn) for btn in row] for row in buttons])


def parse_timer(text: str) -> Tuple[Union[int, None], int]:
    try:
        num = int(text.split(maxsplit=1)[1])
        return abs(num), -1 if num < 0 else 1
    except (ValueError, IndexError):
        return None, 1
