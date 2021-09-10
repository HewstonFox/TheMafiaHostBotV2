from os import path
from typing import List

from bot.controllers import DispatcherProvider
from bot.controllers.ActionController.types import VoteFailReason
from bot.controllers.MessageController import buttons
from bot.controllers.SessionController.settings.constants import DisplayType
from bot.types import ChatId, ResultConfig, RoleMeta
from bot.localization import Localization


class MessageController(DispatcherProvider):

    @classmethod
    async def cleanup_messages(cls, chat_id: ChatId, ids: List[ChatId]):
        for msg_id in ids:
            await cls.dp.bot.delete_message(chat_id, msg_id)

    @classmethod
    async def send_private_start_message(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.private.start, reply_markup=buttons.more(t))

    @classmethod
    async def send_private_more(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.private.more_description)

    @classmethod
    async def send_registration_start(cls, chat_id: ChatId, t: Localization, players: str):
        return await cls.dp.bot.send_message(
            chat_id,
            t.group.registration.start.format(len([x for x in players.split(', ') if x]), players),
            reply_markup=buttons.connect(t)
        )

    @classmethod
    async def update_registration_start(cls, chat_id: ChatId, message_id: int, t: Localization, players: str):
        res = await cls.dp.bot.edit_message_text(
            text=t.group.registration.start.format((len([x for x in players.split(', ') if x])), players),
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=buttons.connect(t),
        )
        return res

    @classmethod
    async def send_registration_is_already_started(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.already_started)

    @classmethod
    async def send_game_is_already_started(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, "*Game is already started")  # todo: add localization

    @classmethod
    async def send_registration_reminder(cls, chat_id: ChatId, t: Localization, time: int, reply_id: ChatId):
        return await cls.dp.bot.send_message(
            chat_id, t.group.registration.reminder.format(time),
            reply_markup=buttons.connect(t),
            reply_to_message_id=reply_id
        )

    @classmethod
    async def send_registration_force_stopped(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.force_stopped)

    @classmethod
    async def send_game_force_stopped(cls, chat_id, t):
        return await cls.dp.bot.send_message(chat_id, "*Game force stopped")  # todo: add localization

    @classmethod
    async def send_registration_skipped(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.skipped)

    @classmethod
    async def send_registration_reduced(cls, chat_id: ChatId, t: Localization, delta: int, time: int):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.reduced.format(delta, time))

    @classmethod
    async def send_registration_extended(cls, chat_id: ChatId, t: Localization, delta: int, time: int):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.extended.format(delta, time))

    @classmethod
    async def send_settings_unavailable_in_game(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, '*Settings unavailable in game')  # todo: add translation

    @classmethod
    async def send_nothing_to_stop(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_nothing_to_skip(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, "*Nothing to skip")  # todo: add localization

    @classmethod
    async def send_nothing_to_reduce(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_nothing_to_extend(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_user_connected_to_game(cls, chat_id: ChatId, t: Localization, session_name: str):
        return await cls.dp.bot.send_message(chat_id, t.private.user_connected.format(session_name))

    @classmethod
    async def send_user_left_game(cls, chat_id: ChatId, t: Localization, session_name: str):
        return await cls.dp.bot.send_message(chat_id, t.private.user_left.format(session_name))

    @classmethod
    async def send_preset_apply_success(cls, chat_id: ChatId, t: Localization, preset: str):
        return await cls.dp.bot.send_message(chat_id, f'*Preset <code>{preset}</code> applied successfully')

    @classmethod
    async def send_role_greeting(cls, chat_id: ChatId, t: Localization, shortcut: str):
        #  todo add localization getting role by shortcut
        try:
            with open(path.join('assets', 'roles', f'{shortcut}.png'), 'rb') as f:
                return await cls.dp.bot.send_photo(chat_id, f, shortcut)
        except FileNotFoundError:
            return await cls.dp.bot.send_message(chat_id, shortcut)

    @classmethod
    async def send_phase_results(cls, chat_id: ChatId, t: Localization, config: ResultConfig, display_type):
        #  todo: add translation
        #  todo: add stickers for each role name
        alive = '\n'.join([f'{role.index}. {role.user.get_mention()}' for role in config['alive']])
        roles = '' if display_type == DisplayType.hide else \
            'Somebody of them:\n' + '\n'.join(
                [f'{k}: {v}' for k, v in config['alive_roles'].items()]
                if display_type == DisplayType.show else [k for k in config['alive_roles']])
        text = f'''
Alive players:
{alive}
        
{roles}
        '''
        return await cls.dp.bot.send_message(chat_id, text)

    @classmethod
    async def send_day(cls, chat_id: ChatId, t: Localization, day_number: int, with_kills: bool = True):
        with open(path.join('assets', 'states', f'day.png'), 'rb') as f:
            #  todo: add translation
            postfix = 'Somebody dead today' if with_kills else 'Nobody dead today'
            return await cls.dp.bot.send_photo(chat_id, f, f'Day {day_number} started.\n{postfix}')

    @classmethod
    async def send_night(cls, chat_id: ChatId, t: Localization):
        with open(path.join('assets', 'states', f'night.png'), 'rb') as f:
            #  todo: add translation
            return await cls.dp.bot.send_photo(chat_id, f, 'Night started', reply_markup=buttons.to_bot(t))

    @classmethod
    async def send_vote(cls, chat_id: ChatId, t: Localization):
        # todo: add translation
        return await cls.dp.bot.send_message(chat_id, 'Voting started', reply_markup=buttons.to_bot(t))

    @classmethod
    async def send_player_left_game(cls, chat_id: ChatId, t: Localization, role: RoleMeta, display_role: bool):
        # todo: add translation
        postfix = f'They were {role.shortcut}' if display_role else ''
        return await cls.dp.bot.send_message(chat_id, f'Player {role.user.get_mention()} left the game. {postfix}')

    @classmethod
    async def send_actor_chose_victim(cls, chat_id: ChatId, t: Localization, actor: str, victim: str):
        # todo: add localization
        return await cls.dp.bot.send_message(chat_id, f'{actor} chose {victim}')

    @classmethod
    async def send_vote_failure_reason(cls, chat_id: ChatId, t: Localization, reason: VoteFailReason):
        if reason is VoteFailReason.no_votes:
            # todo: add localization
            return await cls.dp.bot.send_message(chat_id, 'Players did not nominate a candidate')
        if reason is VoteFailReason.too_much_candidates:
            # todo: add localization
            return await cls.dp.bot.send_message(chat_id, 'The opinion of the townspeople is divided')

    @classmethod
    async def send_mafia_vote_failure_reason(cls, chat_id: ChatId, t: Localization, reason: VoteFailReason):
        if reason is VoteFailReason.too_much_candidates:
            # todo: add localization
            return await cls.dp.bot.send_message(chat_id, 'The opinion of the mafias is divided')

    @classmethod
    async def send_game_results(cls, chat_id: ChatId, t: Localization, team: str, winners: str, losers: str):
        # todo: add localization
        text = f'''
Game ended, winner is {team}
Winners:
{winners}

Losers:
{losers}
        '''
        try:
            with open(path.join('assets', 'results', f'{team}.png'), 'rb') as f:
                return await cls.dp.bot.send_photo(chat_id, f, text)
        except FileNotFoundError:
            return await cls.dp.bot.send_message(chat_id, text)