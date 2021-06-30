from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.types import MarkupKeyboardDict


def arr2keyword_markup(buttons: List[List[MarkupKeyboardDict]]):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(**btn) for btn in row] for row in buttons])
