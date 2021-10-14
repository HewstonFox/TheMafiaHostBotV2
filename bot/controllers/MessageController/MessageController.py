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
        return await cls.dp.bot.send_message(chat_id, t.group.game.already_started)

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
    async def send_game_force_stopped(cls, chat_id, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.game.force_stopped)

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
        return await cls.dp.bot.send_message(chat_id, t.group.game.settings_unavailable)

    @classmethod
    async def send_nothing_to_stop(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.nothing_to_stop)

    @classmethod
    async def send_not_enough_players(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.not_enough_players)

    @classmethod
    async def send_too_much_candidates(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.game.too_much_candidates)

    @classmethod
    async def send_mind_changed(cls, chat_id: ChatId, t: Localization, victim: str):
        return await cls.dp.bot.send_message(chat_id, t.group.game.mind_changed.format(victim))

    @classmethod
    async def send_nothing_to_skip(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.registration.nothing_to_skip)

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
        return await cls.dp.bot.send_message(chat_id, t.group.preset_applied.format(preset))

    @classmethod
    async def send_role_greeting(cls, chat_id: ChatId, t: Localization, shortcut: str):
        try:
            with open(path.join('assets', 'roles', f'{shortcut}.png'), 'rb') as f:
                return await cls.dp.bot.send_photo(chat_id, f, getattr(t.roles, shortcut).greeting)
        except FileNotFoundError:
            return await cls.dp.bot.send_message(chat_id, shortcut)

    @classmethod
    async def send_phase_results(cls, chat_id: ChatId, t: Localization, config: ResultConfig, display_type):
        alive = '\n'.join([f'{role.index}. {role.user.get_mention()}' for role in config['alive']])

        roles = '' if display_type == DisplayType.hide else f'{t.strings.somebody_of_them}\n'

        #  todo: add stickers for each role name
        if display_type == DisplayType.show:
            roles_list = sorted(list(config['alive_roles'].items()), key=lambda x: f'{x[0]}{x[1]}', reverse=True)
            roles += '\n'.join([f'{getattr(t.roles, k).name}: {v}' for k, v in roles_list])
        else:
            roles_list = sorted(list(config['alive_roles']))
            roles += ', '.join([getattr(t.roles, k).name for k in roles_list])

        text = t.group.game.results.format(alive, roles)
        return await cls.dp.bot.send_message(chat_id, text)

    @classmethod
    async def send_day(cls, chat_id: ChatId, t: Localization, day_number: int, with_kills: bool = True):
        with open(path.join('assets', 'states', f'day.png'), 'rb') as f:
            text = t.group.game.day_bad if with_kills else t.group.game.day_good
            return await cls.dp.bot.send_photo(chat_id, f, text.format(day_number))

    @classmethod
    async def send_night(cls, chat_id: ChatId, t: Localization):
        with open(path.join('assets', 'states', f'night.png'), 'rb') as f:
            return await cls.dp.bot.send_photo(chat_id, f, t.group.game.night, reply_markup=buttons.to_bot(t))

    @classmethod
    async def send_vote(cls, chat_id: ChatId, t: Localization):
        return await cls.dp.bot.send_message(chat_id, t.group.game.voting, reply_markup=buttons.to_bot(t))

    @classmethod
    async def send_player_left_game(cls, chat_id: ChatId, t: Localization, role: RoleMeta, display_role: bool):
        text = t.group.game.player_left_game_extended if display_role else t.group.game.player_left_game
        return await cls.dp.bot.send_message(chat_id, text.format(role.user.get_mention(), role.shortcut))

    @classmethod
    async def send_actor_chose_victim(cls, chat_id: ChatId, t: Localization, actor: str, victim: str):
        return await cls.dp.bot.send_message(chat_id, t.group.game.vote_actor_chose_victim.format(actor, victim))

    @classmethod
    async def send_vote_failure_reason(cls, chat_id: ChatId, t: Localization, reason: VoteFailReason):
        if reason is VoteFailReason.no_votes:
            return await cls.dp.bot.send_message(chat_id, t.group.game.no_candidate)
        if reason is VoteFailReason.too_much_candidates:
            return await cls.dp.bot.send_message(chat_id, t.group.game.too_much_candidates)

    @classmethod
    async def send_mafia_vote_failure_reason(cls, chat_id: ChatId, t: Localization, reason: VoteFailReason):
        if reason is VoteFailReason.too_much_candidates:
            return await cls.dp.bot.send_message(chat_id, t.roles.chore.mafia_opinion_divided)

    @classmethod
    async def send_game_results(cls, chat_id: ChatId, t: Localization, team: str, winners: str, losers: str):
        text = t.group.game.endgame.format(*list(map(lambda x: x if x else t.strings.no, (team, winners, losers))))
        try:
            with open(path.join('assets', 'results', f'{team}.png'), 'rb') as f:
                return await cls.dp.bot.send_photo(chat_id, f, text)
        except FileNotFoundError:
            return await cls.dp.bot.send_message(chat_id, text)

    @classmethod
    async def send_role_global_effect(cls, chat_id: ChatId, t: Localization, shortcut: str):
        return await cls.dp.bot.send_message(chat_id, getattr(t.roles, shortcut).global_effect)

    @classmethod
    async def send_role_promotion(cls, chat_id: ChatId, t: Localization, shortcut: str):
        return await cls.dp.bot.send_message(chat_id, getattr(t.roles.chore.promotion, shortcut))

    @classmethod
    async def send_role_affect(cls, chat_id: ChatId, t: Localization, shortcut: str):
        return await cls.dp.bot.send_message(chat_id, getattr(t.roles, shortcut).affect)
