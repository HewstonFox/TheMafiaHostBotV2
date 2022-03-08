from typing import Callable, Any, Union, List

from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageToEditNotFound, MessageNotModified, MessageIdInvalid

from bot.controllers import DispatcherProvider
from bot.controllers.MenuController.types import MessageMenu, MessageMenuButton, ButtonType, MessageMenuButtonOption
from bot.localization import Localization
from bot.types import Proxy, ChatId
from bot.utils.message import arr2keyword_markup
from bot.utils.shared import is_error


class MenuController(DispatcherProvider):
    __sessions = Proxy({})

    @classmethod
    async def show_menu(
            cls,
            chat_id: ChatId,
            config: MessageMenu,
            get_data: Callable[[str], Any],
            set_data: Callable[[str, Any], Union[bool, None]],
            t: Localization
    ):

        session_data = {
            'msg': Message(),  # will be added after first render
            'parents': [],
            'current': config,
            'get': get_data,
            'set': set_data,
            't': t
        }

        if old_menu := cls.__sessions.get(chat_id):
            try:
                await old_menu['msg'].delete()
            except:
                pass

        cls.__sessions[chat_id] = session_data
        await cls.render(chat_id)
        await session_data['msg'].pin()

    @classmethod
    def get_reply_markup(
            cls,
            buttons: List[Union[MessageMenuButton, MessageMenuButtonOption]],
            get_data,
            t: Localization,
            parent: MessageMenuButton = None,
            current: MessageMenuButton = None,
    ):
        reply_markup = []
        for i, btn in enumerate(buttons):
            tp = btn.get('type')
            if tp in (ButtonType.route, ButtonType.select):  # routing buttons
                reply_markup.append([{'text': btn['name'], 'callback_data': f'menu route {i}'}])
            elif tp == ButtonType.int:
                reply_markup.extend([
                    [{'text': str(get_data(btn['key'])), 'callback_data': '_'}],
                    [
                        {'text': '-5', 'callback_data': f'menu mutate {i} -5'},
                        {'text': '+5', 'callback_data': f'menu mutate {i} +5'},
                    ],
                    [
                        {'text': '-1', 'callback_data': f'menu mutate {i} -1'},
                        {'text': '+1', 'callback_data': f'menu mutate {i} +1'},
                    ]
                ])
            elif tp == ButtonType.float:
                reply_markup.extend([
                    [{'text': str(get_data(btn['key'])), 'callback_data': '_'}],
                    [
                        {'text': '-1', 'callback_data': f'menu mutate {i} -1'},
                        {'text': '+1', 'callback_data': f'menu mutate {i} +1'},
                    ],
                    [
                        {'text': '-0.1', 'callback_data': f'menu mutate {i} -0.1'},
                        {'text': '+0.1', 'callback_data': f'menu mutate {i} +0.1'},
                    ]
                ])
            elif tp == ButtonType.decimal:
                reply_markup.extend([
                    [{'text': str(get_data(btn['key'])), 'callback_data': '_'}],
                    [
                        {'text': '-1', 'callback_data': f'menu mutate {i} -1'},
                        {'text': '+1', 'callback_data': f'menu mutate {i} +1'},
                    ],
                    [
                        {'text': '-0.1', 'callback_data': f'menu mutate {i} -0.1'},
                        {'text': '+0.1', 'callback_data': f'menu mutate {i} +0.1'},
                    ],
                    [
                        {'text': '-0.01', 'callback_data': f'menu mutate {i} -0.01'},
                        {'text': '+0.01', 'callback_data': f'menu mutate {i} +0.01'},
                    ]
                ])
            elif tp == ButtonType.toggle:
                value = get_data(btn['key'])
                display = tmp[0] if len(
                    tmp := [opt['name'] for opt in btn['options'] if opt['value'] == value]) else value
                reply_markup.append([{'text': f'☛ {str(display)} ☚', 'callback_data': f'menu mutate {i}'}])
            elif tp == ButtonType.endpoint:
                reply_markup.append([{'text': btn['name'], 'callback_data': f'menu mutate {i}'}])
            else:  # option button and it has 'select' parent
                value = get_data(current['key'])
                str_wrapper = '☛ {}' if value == btn['value'] else '{}'
                reply_markup.append([{'text': str_wrapper.format(btn['name']), 'callback_data': f'menu mutate {i}'}])

        if not current.get('disable_special_buttons'):
            if parent:
                reply_markup.append([{'text': f'🔙 {t.strings.back}', 'callback_data': f'menu back'}])
            else:
                reply_markup.append([{'text': f'❌ {t.strings.close}', 'callback_data': f'menu close'}])
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

        try:
            i = int(keys[1])
            if way == 'route':
                await cls.router(chat_id, i)
                return await query.answer()
            if way == 'mutate':
                return await cls.mutator(chat_id, i, keys[2:], query)
        except (KeyError, IndexError):
            try:
                await cls.render(chat_id)
            except KeyError:
                pass

    @classmethod
    async def close(cls, chat_id: ChatId):
        if chat_id in cls.__sessions:
            session = cls.__sessions[chat_id]
            del cls.__sessions[chat_id]
            await session['msg'].delete()

    @classmethod
    async def back(cls, chat_id):
        session = cls.__sessions[chat_id]
        try:
            session['current'] = session['parents'].pop()
            await cls.render(chat_id)
        except IndexError:
            await cls.close(chat_id)

    @classmethod
    async def mutator(cls, chat_id: ChatId, i: int, meta: List[str], query: CallbackQuery):
        session = cls.__sessions[chat_id]
        current = session['current']
        set_data = session['set']
        get_data = session['get']
        if current.get('type') == ButtonType.select:
            key = current['key']
            current_value = get_data(key)
            value = current['options'][i]['value']
        else:
            btn = current['buttons'][i]
            key = btn.get('key')
            if not key:
                return await query.answer()
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
                _min = btn.get('min')
                _max = btn.get('max')
                delta = parser(meta[0])
                value = round(current_value + delta, 4)
                if (_max and value > _max) or (_min and value < _min):
                    return await query.answer()
            elif tp == ButtonType.endpoint:
                description = get_data(key)
                res = set_data(key, None)
                if res is None or res:
                    await session['msg'].edit_text(description)
                    await session['msg'].unpin()
                    cls.__sessions.pop(chat_id)
                    return await query.answer()
                else:
                    return await query.answer(description)

            else:
                return await query.answer()

        if value == current_value:
            return await query.answer()

        res = set_data(key, value)
        if res is None or res:
            await cls.render(chat_id)

        return await query.answer()

    @classmethod
    async def router(cls, chat_id: ChatId, i: int):
        session = cls.__sessions[chat_id]
        try:
            route = session['current']['buttons'][i]
            session['parents'].append(session['current'])
            session['current'] = route
            await cls.render(chat_id)
        except IndexError:
            return

    @classmethod
    async def render(cls, chat_id: ChatId, new: bool = False):
        session = cls.__sessions[chat_id]
        params = {
            'text': session['current']['description'],
            'reply_markup': cls.get_reply_markup(
                session['current'].get(
                    'options' if session['current'].get('type') == ButtonType.select else 'buttons') or [],
                session['get'],
                session['t'],
                session['parents'][-1] if len(session['parents']) else None,
                session['current'],
            )
        }
        try:
            if new:
                raise MessageToEditNotFound
            res = await session['msg'].edit_text(**params)
            if is_error(res):
                raise res
        except (MessageToEditNotFound, AttributeError, MessageIdInvalid):
            session['msg'] = await cls.dp.bot.send_message(chat_id, **params)
        except MessageNotModified:
            pass
