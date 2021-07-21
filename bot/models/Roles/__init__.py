from typing import Type

from bot.models.Roles import Civil, Don, Mafia, Commissioner, Doctor, Suicide, Whore, Bum, Lawyer, Lucky, Maniac
from bot.models.Roles.BaseRole import BaseRole

Roles = BaseRole.__subclasses__()


def get_cap(cls: Type[BaseRole]):
    return cap[0] if len(cap := [x for x in cls.__subclasses__() if x != BaseRole]) else None
