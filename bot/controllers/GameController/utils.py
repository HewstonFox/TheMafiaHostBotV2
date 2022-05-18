import asyncio
from random import shuffle
from typing import Optional, Iterable, Callable, Any, Awaitable, Union

from aiogram.types import User
from aiogram.utils.exceptions import Unauthorized

from bot.controllers.ActionController.ActionController import ActionController
from bot.controllers.ActionController.Actions.VoteAction import MafiaKillVoteAction, VoteAction
from bot.controllers.ActionController.types import VoteFailReason
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.types import SessionStatus, RolesList
from bot.models.Roles import Roles, get_cap, Incognito, BaseRole
from bot.models.Roles.Civil import Civil
from bot.models.Roles.Commissioner import Commissioner
from bot.models.Roles.Mafia import Mafia
from bot.models.Roles.constants import Team
from bot.types import ResultConfig, RoleMeta
from bot.utils.message import attach_mafia_chat as amc


def attach_roles(session: Session):
    players = session.players.values()
    settings = session.settings.values['roles']
    roles = []
    players_count = len(players)

    for role in [
        role for role in Roles
        if role != Civil and (settings[role.shortcut].get('enable') is None or settings[role.shortcut].get('enable'))
    ]:
        _roles = [role] * int(players_count / settings[role.shortcut]['n'] + 0.5)
        if (cap := get_cap(role)) and len(_roles):
            _roles[0] = cap
        roles.extend(_roles)

    roles = sorted(roles, key=lambda x: x != Mafia)
    roles = roles[:players_count]
    if (difference := players_count - len(roles)) > 0:
        roles.extend([Civil] * difference)

    shuffle(roles)

    index = 1
    for user, role in zip(players, roles):
        session.roles[user.id] = role(user, session, index)
        index += 1


async def private_message_error_wrapper(task: Awaitable, session: Session, user: User):
    try:
        return await task
    except Unauthorized:
        session.remove_player(user.id)


async def greet_roles(session: Session):
    await asyncio.wait(
        [private_message_error_wrapper(role.greet(), session, role.user) for role in session.roles.values()])


async def send_roles_vote(session: Session):
    await MessageController.send_vote(session.chat_id, session.t)
    players: list[Incognito] = list(session.roles.values())  # just for typehint
    await asyncio.wait([player.send_vote() for player in players if player.alive])


def get_session_winner(alive: list[Union[BaseRole, RoleMeta]]) -> Optional[str]:
    if (alive_count := len(alive)) > 2:
        angry_roles = [role for role in alive if role.is_angry]
        if len(angry_roles) == 0:
            return Team.civ

        mafia_count = len([role for role in alive if role.team == Team.maf])
        if mafia_count >= (alive_count - mafia_count):
            return Team.maf
    elif alive_count == 1:
        return alive[0].team
    elif alive_count == 0:
        return Team.BOTH
    else:
        a, b = alive
        if a.team == b.team == Team.civ:
            return Team.civ
        if a.team == b.team == Team.maf:
            return Team.maf
        if a.is_angry and b.is_angry:
            return Team.BOTH
        if isinstance(a, Commissioner) or isinstance(b, Commissioner):
            return Team.BOTH
        if a.is_angry:
            return a.team
        if b.is_angry:
            return b.team
        return Team.civ


def get_result_config(session: Session) -> ResultConfig:
    config = {
        'alive': [],
        'dead': [],
        'alive_roles': {}
    }
    for player in session.roles.values():
        config['alive' if player.alive else 'dead'].append(player)
        if not player.alive:
            continue
        if player.shortcut not in config['alive_roles']:
            config['alive_roles'][player.shortcut] = 0
        config['alive_roles'][player.shortcut] += 1

    return config


async def resolve_results(session: Session, store: dict):
    result_config = get_result_config(session)
    winner = get_session_winner(result_config['alive'])
    store['config'] = result_config
    store['winner'] = winner


async def run_tasks(session: Session, tasks: Iterable[Callable[[], Any]]):
    for task in tasks:
        if session.status != SessionStatus.game:
            return
        if not task:
            continue
        tmp = task()
        if isinstance(tmp, Awaitable):
            await tmp


async def resolve_schedules(tasks: Optional[Iterable[Callable[[], Any]]]):
    if not tasks:
        return
    for task in tasks:
        tmp = task()
        if isinstance(tmp, Awaitable):
            await tmp


async def show_game_state(session: Session, config: Optional[ResultConfig]):
    if not config:
        return
    await MessageController.send_phase_results(
        session.chat_id,
        session.t,
        config,
        session.settings.values['game']['show_live_roles']
    )


async def send_game_phase(session: Session, cross_pipeline_store: dict):
    if cross_pipeline_store['winner']:
        return
    if session.is_night:
        await MessageController.send_night(session.chat_id, session.t)
    else:
        await MessageController.send_day(
            session.chat_id, session.t, session.day_count,
            bool(cross_pipeline_store.get('just_dead'))
        ),


async def send_roles_actions(session: Session):
    await asyncio.wait(
        [private_message_error_wrapper(role.send_action(), session, role.user) for role in session.roles.values() if
         role.alive])


async def promote_roles_if_need(roles: RolesList):
    for role in [role for role in roles.values() if role.alive]:
        if (cap := get_cap(type(role))) and not any(isinstance(r, cap) for r in roles.values() if r.alive):
            roles[role.user.id] = cap(role.user, role.session, role.index)
            await private_message_error_wrapper(roles[role.user.id].send_promotion(), role.session, role.user)


async def apply_actions(session: Session, store: dict):
    store['vote_fails_reasons'] = await ActionController.apply_actions(session.roles)


async def attach_mafia_chat(session: Session):
    if not session.settings.values['game']['allow_mafia_chat']:
        return

    session.mafia_chat_handler = await amc([role for role in session.roles.values() if role.team == Team.maf])


async def resolve_failure_votes(session: Session, failure_votes: dict[VoteAction, Optional[VoteFailReason]]):
    for vote_type, reason in failure_votes.items():
        if vote_type == MafiaKillVoteAction:
            for pl in session.roles.values():
                if pl is not Mafia:
                    continue
                await MessageController.send_mafia_vote_failure_reason(pl.user.id, session.t, reason)
