from typing import TypedDict, List, Dict, Union

from aiogram.types import User

ChatId = Union[int, str]


class SessionStatus:
    registration = 'registration'
    game = 'game'
    pending = 'pending'  # delete if unnecessary
    end = 'end'  # delete if unnecessary


class KilledPlayerData(TypedDict):
    user: User
    role: None  # todo replace with role type


KilledPlayersList = List[KilledPlayerData]

PlayersList = Dict[Union[str, int], User]

RolesList = Dict[Union[str, int], None]  # todo replace with role type


class CallbackQueryActions:
    add_player = 'add_player'
    role_action = 'role_action'
    vote_user = 'vote_user'
    vote_agree = 'vote_agree'
    faq = 'faq'


class ChatType:
    private = 'private'
    group = 'group'
    supergroup = 'supergroup'
    channel = 'channel'
