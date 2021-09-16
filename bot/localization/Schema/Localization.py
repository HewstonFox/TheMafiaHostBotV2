from dataclasses import dataclass

from dict_to_dataclass import DataclassFromDict, field_from_dict

from bot.localization.Schema.CallbackQuery import LCallbackQuery
from bot.localization.Schema.Commands import LCommands
from bot.localization.Schema.Group import LGroup
from bot.localization.Schema.Private import LPrivate
from bot.localization.Schema.Strings import LStrings


@dataclass
class Localization(DataclassFromDict):
    Locale: str = field_from_dict()
    language: str = field_from_dict()
    private: LPrivate = field_from_dict()
    group: LGroup = field_from_dict()
    callback_query: LCallbackQuery = field_from_dict()
    commands: LCommands = field_from_dict()
    strings: LStrings = field_from_dict()
