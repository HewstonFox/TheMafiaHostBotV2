import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.types import User, ChatMemberStatus
from schema import SchemaError

from bot.controllers.MenuController.MenuController import MenuController
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.settings.Settings import Settings
from bot.controllers.SessionController.settings.settings_config import get_settings_menu_config
from bot.controllers.SessionController.types import PlayersList, RolesList, SessionStatus, \
    SessionRecord
from bot.controllers.SessionController import collection
from bot.models import MafiaBotError
from bot.models.MafiaBotError import InvalidSessionStatusError
from bot.types import ChatId, Proxy
from bot.localization import Localization, get_translation, get_default_translation_index
from bot.utils.restriction import restriction_with_prev_state, SEND_RESTRICTIONS


class Session:

    def __init__(
            self, *,
            chat_id: ChatId,
            lang: str = None,
            name: str = '',
            invite_url: str = '',
            status: str = SessionStatus.pending,
            settings: dict = {},
            **kwargs
    ):
        if int(chat_id) > 0:
            raise MafiaBotError.InvalidSessionIdError
        self.chat_id: ChatId = chat_id
        self.name = name
        self.players: PlayersList = Proxy({})
        self.roles: RolesList = Proxy({})
        _lang = lang or settings.get('language') or get_default_translation_index()
        self.t: Localization = get_translation(_lang)
        self.handlers = []
        self.restrictions: dict[ChatId, dict] = {}
        self.invite_url = invite_url
        self.__status: str = status
        if 'bot' in kwargs:
            self.bot = kwargs['bot']

        try:
            if not settings:
                raise SchemaError("Settings not provided")
            self.settings = Settings(config=settings)
        except SchemaError:
            self.settings = Settings(lang=_lang)
        self.is_night = self.settings.values['game']['start_at_night']
        self.day_count = 0
        self.timer: int = 0
        self.mafia_chat_handler = None
        self.dp: Optional[Dispatcher] = None

    def add_player(self, user: User):
        self.players[user.id] = user

    def is_user_in(self, user_id: ChatId):
        return user_id in self.players

    def remove_player(self, user_id):
        self.players.pop(user_id)
        if self.status == SessionStatus.game:
            self.roles[user_id].alive = False
            self.roles[user_id].won = False
            asyncio.create_task(MessageController.send_player_left_game(
                self.chat_id,
                self.t,
                self.roles[user_id],
                self.settings.values['game']['show_role_of_departed']
            ))

    def __del__(self):
        self.status = SessionStatus.pending

    async def restrict_role(self, chat_id: ChatId):
        if self.__status != SessionStatus.game or chat_id not in self.roles or chat_id in self.restrictions:
            return
        self.restrictions[chat_id] = await restriction_with_prev_state(
            self.bot,
            self.chat_id,
            chat_id,
            SEND_RESTRICTIONS
        )

    async def __watch_chat_members(self):
        bot: Bot = self.bot
        if not bot:
            return
        while self.status != SessionStatus.pending:
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
        self.__status = value
        self.update()
        if value == SessionStatus.registration:
            asyncio.create_task(self.__watch_chat_members())

    def toggle(self):
        self.is_night ^= True
        if not self.is_night:
            self.day_count += 1

    def update_settings(self, key: str, value):
        res = self.settings.set_property(key, value)
        if res and key == 'language':
            self.t = get_translation(value)  # hot localization update
        self.update()
        return res

    @classmethod
    async def get_by_chat_id(cls, chat_id: ChatId):
        session_record = await collection.get_session_record_by_chat_id(chat_id)
        return Session(**session_record) if session_record else None

    @classmethod
    async def create(cls, **kwargs):
        record: SessionRecord = await collection.create_session_record(**kwargs)
        return Session(**record)

    def apply_settings_preset(self, preset: str):
        self.settings.apply_preset(preset)
        self.update()

    def import_settings_from_file(self, file):
        self.settings.apply_from_file(file)
        self.update()

    async def show_settings_menu(self):
        if self.status != SessionStatus.pending:
            await MessageController.send_settings_unavailable_in_game(self.chat_id, self.t)
            return
        config = get_settings_menu_config(self.t)
        getter = self.settings.get_property
        setter = self.update_settings

        await MenuController.show_menu(self.chat_id, config, getter, setter, self.t)

    def update(self):
        data = {
            'name': self.name,
            'status': self.status,
            'settings': self.settings.values,
            'invite_url': self.invite_url
        }
        asyncio.create_task(collection.update_session_record(self.chat_id, data))

    def __repr__(self):
        return str(self.__dict__)

    def get_dump(self):
        return {
            **{k: v for k, v in self.__dict__.items() if
               k not in ('t', 'bot', 'players', 'handlers', 'mafia_chat_handler', 'dp')},
            'players': {idx: user.to_python() for idx, user in self.players.items()}
        }
