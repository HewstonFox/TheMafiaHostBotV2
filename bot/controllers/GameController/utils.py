import asyncio
from random import shuffle
from typing import Optional, Iterable, Callable, Any, Awaitable

from bot.controllers.ActionController.ActionController import ActionController
from bot.controllers.ActionController.Actions.VoteAction import DayKillVoteAction, MafiaKillVoteAction, VoteAction
from bot.controllers.ActionController.types import VoteFailReason
from bot.controllers.MessageController.MessageController import MessageController
from bot.controllers.SessionController.Session import Session
from bot.controllers.SessionController.types import SessionStatus
from bot.models.Roles import Roles, get_cap, Incognito, BaseRole
from bot.models.Roles.Civil import Civil
from bot.models.Roles.Commissioner import Commissioner
from bot.models.Roles.Don import Don
from bot.models.Roles.Mafia import Mafia
from bot.models.Roles.Maniac import Maniac
from bot.models.Roles.constants import Team
from bot.types import ResultConfig
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

    print(session.roles)  # todo: remove


async def greet_roles(session: Session):
    await asyncio.wait([role.greet() for role in session.roles.values()])


async def send_roles_vote(session: Session):
    await MessageController.send_vote(session.chat_id, session.t)
    players: list[Incognito] = list(session.roles.values())  # just for typehint
    await asyncio.wait([player.send_vote() for player in players if player.alive])


async def get_session_winner(config: dict) -> Optional[str]:
    alive: list[BaseRole] = config['alive']
    if (alive_count := len(alive)) > 2:
        mafia_count = len([mafia for mafia in alive if isinstance(mafia, Mafia)])
        if not mafia_count:
            return Team.civ
        peace_count = alive_count - mafia_count
        if mafia_count >= peace_count:
            return Team.maf
    else:
        danger_roles = Mafia, Don, Maniac
        a, b = alive
        type_a = type(a)
        type_b = type(b)
        is_danger_a = type_a in danger_roles
        is_danger_b = type_b in danger_roles
        if a.team == b.team == Team.civ:
            return a.team
        elif is_danger_a != is_danger_b and Commissioner not in (type_a, type_b):
            return a.team if is_danger_a else b.team
        return Mafia.team if a.team == b.team == Team.maf else Team.BOTH


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
    winner = await get_session_winner(result_config)
    store['config'] = result_config
    store['winner'] = winner


async def run_tasks(session: Session, tasks: Iterable[Callable[[], Any]]):
    for task in tasks:
        if session.status != SessionStatus.game:
            return
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
    await asyncio.wait([role.send_action() for role in session.roles.values() if role.alive])


async def promote_roles_if_need(session: Session):
    for role in list(session.roles.values())[:]:
        if (cap := get_cap(type(role))) and not any(isinstance(r, cap) for r in session.roles.values()):
            session.roles[role.user.id] = cap(role.user, session, role.index)
            await session.roles[role.user.id].send_promotion()


async def apply_actions(session: Session, store: dict):
    store['vote_fails_reasons'] = await ActionController.apply_actions(session.roles)


async def attach_mafia_chat(session: Session):
    if not session.settings.values['game']['allow_mafia_chat']:
        return

    await amc([role for role in session.roles.values() if isinstance(role, Mafia)])


async def resolve_failure_votes(session: Session, failure_votes: dict[VoteAction, Optional[VoteFailReason]]):
    for vote_type, reason in failure_votes.items():
        if vote_type == MafiaKillVoteAction:
            for pl in session.roles.values():
                if pl is not Mafia:
                    continue
                await MessageController.send_mafia_vote_failure_reason(pl.user.id, session.t, reason)
