import asyncio

from aiogram import Bot
from aiogram.types import User

from bot.controllers.SessionController.types import PlayersList, RolesList, KilledPlayersList, SessionStatus, \
    SessionRecord
from bot.controllers.SessionController import collection
from bot.models import MafiaBotError
from bot.models.MafiaBotError import InvalidSessionStatusError
from bot.types import ChatId
from bot.localization import Localization, get_translation


class Session:
    def __init__(self,
                 chat_id: ChatId,
                 name: str = '',
                 status: str = SessionStatus.pending,
                 lang: str = 'en',
                 **kwargs
                 ):
        if int(chat_id) > 0:
            raise MafiaBotError.InvalidSessionIdError
        self.chat_id: ChatId = chat_id
        self.name = name
        self.players: PlayersList = {}
        self.roles: RolesList = {}
        self.killed: KilledPlayersList = []
        self.t: Localization = get_translation(lang)
        self.__status: str = status
        if 'bot' in kwargs:
            self.bot = kwargs['bot']

    def add_player(self, user: User):
        self.players[user.id] = user
        print(self.players)

    def is_user_in(self, user_id: ChatId):
        return user_id in self.players

    def remove_player(self, user_id):
        if self.status == SessionStatus.registration:
            self.players.pop(user_id)

    def __del__(self):
        self.status = SessionStatus.pending

    async def __watch_chat_members(self):
        bot: Bot = self.bot
        if not bot:
            return
        end_statuses = (SessionStatus.pending, SessionStatus.end)
        while self.status not in end_statuses:
            for player_id in list(self.players):
                if not (await bot.get_chat_member(self.chat_id, player_id)).is_chat_member():
                    self.remove_player(player_id)
            await asyncio.sleep(1)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in SessionStatus.__dict__.values():
            raise InvalidSessionStatusError
        asyncio.create_task(self.update(status=value))
        self.__status = value
        if value == SessionStatus.registration:
            asyncio.create_task(self.__watch_chat_members())

    @classmethod
    async def get_by_chat_id(cls, chat_id: ChatId):
        session_record = await collection.get_session_record_by_chat_id(chat_id)
        return Session(**session_record) if session_record else None

    @classmethod
    async def create(cls, **kwargs):
        record: SessionRecord = await collection.create_session_record(**kwargs)
        return Session(**record)

    async def update(self, *_, **kwargs):
        data = {}
        if 'name' in kwargs:
            data['name'] = kwargs['name']
        if 'status' in kwargs:
            data['status'] = kwargs['status']
        if 'lang' in kwargs:
            data['lang'] = kwargs['lang']

        record = await collection.update_session_record(self.chat_id, data)
        self.__status = record['status']
        self.name = record['name']
        self.t = get_translation(record['lang'])
