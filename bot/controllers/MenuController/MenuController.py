from typing import Callable, Any, Union, List

from aiogram.types import CallbackQuery

from bot.controllers import BaseController
from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType, MessageMenuButtonOption
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.SessionController import SessionController
from bot.controllers.SessionController.types import SessionStatus
from bot.models.MafiaBotError import SessionAlreadyActiveError
from bot.types import Proxy, ChatId
from bot.utils.message import arr2keyword_markup


class MenuController(BaseController):
    __sessions = Proxy({})

    @classmethod
    async def show_menu(
            cls,
            session: Session,
            config: MessageMenu,
            get_data: Callable[[str], Any],
            set_data: Callable[[str, Any], Union[bool, None]]
    ):
        session.status = SessionStatus.settings
        try:
            SessionController.push_session(session)
        except SessionAlreadyActiveError:
            # todo: send again if message loosed, unpin and pin if message exists
            return
        msg = await cls.build_menu(session.chat_id, config, get_data)
        cls.__sessions[session.chat_id] = {
            'msg': msg,
            'parents': [],
            'current': config,
            'get': get_data,
            'set': set_data
        }

    @classmethod
    async def build_menu(cls, chat_id: ChatId, config: MessageMenu, get_data):
        return await cls.dp.bot.send_message(
            chat_id,
            config['description'],
            reply_markup=cls.get_reply_markup(config['buttons'], get_data)
        )

    @classmethod
    def get_reply_markup(
            cls,
            buttons: List[Union[MessageMenuButton, MessageMenuButtonOption]],
            get_data,
            parent: MessageMenuButton = None,
            current: MessageMenuButton = None
    ):
        reply_markup = []
        for i, btn in enumerate(buttons):
            tp = btn.get('type')
            if tp in (ButtonType.route, ButtonType.select):  # routing buttons
                reply_markup.append([{'text': btn['name'], 'callback_data': f'menu route {i}'}])
            elif tp == ButtonType.int:
                reply_markup.append([
                    {'text': '-5', 'callback_data': f'menu mutate {i} -5'},
                    {'text': '-1', 'callback_data': f'menu mutate {i} -1'},
                    {'text': str(get_data(btn['key'])), 'callback_data': f'menu mutate {i}'},
                    {'text': '+1', 'callback_data': f'menu mutate {i} +1'},
                    {'text': '+5', 'callback_data': f'menu mutate {i} +5'},
                ])
            elif tp == ButtonType.float:
                reply_markup.append([
                    {'text': '-1', 'callback_data': f'menu mutate {i} -1'},
                    {'text': '-0.1', 'callback_data': f'menu mutate {i} -0.1'},
                    {'text': str(get_data(btn['key'])), 'callback_data': f'menu mutate {i}'},
                    {'text': '+0.1', 'callback_data': f'menu mutate {i} +0.1'},
                    {'text': '+1', 'callback_data': f'menu mutate {i} +1'},
                ])
            elif tp == ButtonType.decimal:
                reply_markup.append([
                    {'text': '-1', 'callback_data': f'menu mutate {i} -1'},
                    {'text': '-0.1', 'callback_data': f'menu mutate {i} -0.1'},
                    {'text': '-0.01', 'callback_data': f'menu mutate {i} -0.01'},
                    {'text': str(get_data(btn['key'])), 'callback_data': f'menu mutate {i}'},
                    {'text': '+0.01', 'callback_data': f'menu mutate {i} +0.01'},
                    {'text': '+0.1', 'callback_data': f'menu mutate {i} +0.1'},
                    {'text': '+1', 'callback_data': f'menu mutate {i} +1'},
                ])
            elif tp == ButtonType.toggle:
                value = get_data(btn['key'])
                display = tmp[0] if len(
                    tmp := [opt['name'] for opt in btn['options'] if opt['value'] == value]) else value
                reply_markup.append([{'text': str(display), 'callback_data': f'menu mutate {i}'}])
            else:  # option button and it has 'select' parent
                value = get_data(current['key'])
                str_wrapper = '☛ {}' if value == btn['value'] else '{}'
                reply_markup.append([{'text': str_wrapper.format(btn['name']), 'callback_data': f'menu mutate {i}'}])

        if parent:
            reply_markup.append([{'text': '🔙 Back', 'callback_data': f'menu back'}])  # todo: add translation
        else:
            reply_markup.append([{'text': '❌ Close', 'callback_data': f'menu close'}])  # todo: add translation
        return arr2keyword_markup(reply_markup)

    @classmethod
    async def callback_handler(cls, query: CallbackQuery):
        chat_id = query.message.chat.id
        if chat_id not in cls.__sessions or cls.__sessions[chat_id]['msg'].message_id != query.message.message_id:
            await query.message.delete()
            return await query.answer()

        keys = query.data.split()[1:]
        way = keys[0]
        if way == 'close':
            await cls.close(chat_id)
            return await query.answer()
        if way == 'back':
            await cls.back(chat_id)
            return await query.answer()

        i = int(keys[1])
        if way == 'route':
            await cls.router(chat_id, i)
            return await query.answer()
        if way == 'mutate':
            await cls.mutator(chat_id, i, keys[2:])
            return await query.answer()

    @classmethod
    async def close(cls, chat_id: ChatId):
        if chat_id in cls.__sessions:
            session = cls.__sessions[chat_id]
            del cls.__sessions[chat_id]
            try:
                SessionController.kill_session(chat_id)
            except KeyError:
                pass
            await session['msg'].delete()

    @classmethod
    async def back(cls, chat_id):
        session = cls.__sessions[chat_id]
        session['current'] = session['parents'].pop()
        await cls.rerender(chat_id)

    @classmethod
    async def mutator(cls, chat_id: ChatId, i: int, meta: List[str]):
        session = cls.__sessions[chat_id]
        current = session['current']
        set_data = session['set']
        get_data = session['get']
        if current['type'] == ButtonType.select:
            key = current['key']
            current_value = get_data(key)
            value = current['options'][i]['value']
        else:
            btn = current['buttons'][i]
            key = btn.get('key')
            if not key:
                return
            tp = btn['type']
            current_value = get_data(key)
            if tp == ButtonType.toggle:
                i = tmp + 1 if (
                        (tmp := [i for i, opt in enumerate(btn['options']) if opt['value'] == current_value][0])
                        < len(btn['options']) - 1
                ) else 0
                value = btn['options'][i]['value']
            elif tp in (ButtonType.int, ButtonType.float, ButtonType.decimal):
                parser = int if tp == ButtonType.int else float
                delta = parser(meta[0])
                value = current_value + delta
            else:
                return

        if value == current_value:
            return

        res = set_data(key, value)
        if res is None or res:
            await cls.rerender(chat_id)

    @classmethod
    async def router(cls, chat_id: ChatId, i: int):
        session = cls.__sessions[chat_id]
        try:
            route = session['current']['buttons'][i]
            session['parents'].append(session['current'])
            session['current'] = route
            await cls.rerender(chat_id)
        except IndexError:
            return

    @classmethod
    async def rerender(cls, chat_id: ChatId):
        session = cls.__sessions[chat_id]
        await session['msg'].edit_text(
            session['current']['description'],
            reply_markup=cls.get_reply_markup(
                session['current']['options' if session['current'].get('type') == ButtonType.select else 'buttons'],
                session['get'],
                session['parents'][-1] if len(session['parents']) else None,
                session['current']
            )
        )
