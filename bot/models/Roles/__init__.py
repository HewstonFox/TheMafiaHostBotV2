from typing import Type

from bot.models.Roles import \
    Civil, \
    Don, Mafia, \
    Commissioner, Sergeant, \
    Doctor, \
    Suicide, \
    Whore, \
    Bum, \
    Lawyer, \
    Lucky, \
    Maniac
from bot.models.Roles.BaseRole import BaseRole
from bot.models.Roles.Incognito import Incognito

Roles = Incognito.__subclasses__()


def get_cap(cls: Type[BaseRole]):
    return cap[0] if len(cap := [x for x in cls.__subclasses__() if x != BaseRole and x != Incognito]) else None
