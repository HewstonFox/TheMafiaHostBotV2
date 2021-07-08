import asyncio

from aiogram import Bot
from aiogram.types import User, ChatMemberStatus
from schema import SchemaError

from bot.controllers.SessionController.settings.Settings import Settings
from bot.controllers.SessionController.types import PlayersList, RolesList, KilledPlayersList, SessionStatus, \
    SessionRecord
from bot.controllers.SessionController import collection
from bot.models import MafiaBotError
from bot.models.MafiaBotError import InvalidSessionStatusError
from bot.types import ChatId, Proxy
from bot.localization import Localization, get_translation, get_default_translation_index


class Session:

    def __init__(self, *,
                 chat_id: ChatId,
                 lang: str = None,
                 name: str = '',
                 status: str = SessionStatus.pending,
                 settings: dict = None,
                 **kwargs
                 ):
        if int(chat_id) > 0:
            raise MafiaBotError.InvalidSessionIdError
        self.chat_id: ChatId = chat_id
        self.name = name
        self.players: PlayersList = Proxy({})
        self.roles: RolesList = Proxy({})
        self.killed: KilledPlayersList = []
        _lang = lang or settings.get('language') or get_default_translation_index()
        self.t: Localization = get_translation(_lang)

        self.__status: str = status
        if 'bot' in kwargs:
            self.bot = kwargs['bot']

        try:
            if not settings:
                raise SchemaError
            self.settings = Settings(config=settings)
        except SchemaError:
            self.settings = Settings(lang=_lang)

        self.timer: int = 0

    def add_player(self, user: User):
        self.players[user.id] = user

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
                if (await bot.get_chat_member(self.chat_id, player_id)).status in (
                        ChatMemberStatus.BANNED, ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
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
        if 'settings' in kwargs:
            data['settings'] = kwargs['setting']

        record = await collection.update_session_record(self.chat_id, data)
        self.__status = record['status']
        self.name = record['name']
        self.t = get_translation(record['settings']['language'])
        self.settings = Settings(config=record['settings'])

    def __repr__(self):
        return str(self.__dict__)
