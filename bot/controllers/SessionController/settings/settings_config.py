from bot.controllers.MenuController.types import ButtonType, MessageMenu, \
    MessageMenuButton as Btn, \
    MessageMenuButtonOption as Opt
from bot.localization import Localization, get_all_translations
from bot.controllers.SessionController.settings.constants import *


def get_time_limits_by_key(key: str):
    if key == 'registration':
        return registration_min, None
    if key in ('extend', 'reduce'):
        return registration_change_time_min, None
    if key == 'night':
        return night_min, None
    if key == 'day':
        return day_min, None
    if key == 'poll':
        return poll_min, None
    if key == 'vote':
        return vote_min, None


def command_route_button(t, command) -> Btn:
    return Btn(
        type=ButtonType.route,
        name=command,
        description=getattr(t, command),
        buttons=[
            Btn(
                type=ButtonType.toggle,
                key=f'command_rights.{command}',
                options=[
                    Opt(
                        name=t.options.all,
                        value=False,
                    ),
                    Opt(
                        name=t.options.admin_only,
                        value=True,
                    ),
                ]
            )
        ]
    )


def time_route_button(t, key):
    _min, _max = get_time_limits_by_key(key)
    return Btn(
        type=ButtonType.route,
        name=getattr(t, key).name,
        description=getattr(t, key).description,
        buttons=[
            Btn(
                type=ButtonType.int,
                key=f'time.{key}',
                min=_min,
                max=_max,
            )
        ]
    )


def players_route_button(t, key):
    return Btn(
        type=ButtonType.route,
        name=getattr(t, key).name,
        description=getattr(t, key).description,
        buttons=[
            Btn(
                type=ButtonType.int,
                key=f'players.{key}',
                min=min_players,
            )
        ]
    )


def game_toggle_button(t, key):
    return Btn(
        type=ButtonType.route,
        name=getattr(t.values, key),
        description=getattr(t.values, key),
        buttons=[Btn(
            type=ButtonType.toggle,
            key=f'game.{key}',
            options=[
                Opt(
                    name=t.options.enable,
                    value=True
                ),
                Opt(
                    name=t.options.disable,
                    value=False
                )
            ]
        )]
    )


def role_route_button(t, key):
    return Btn(
        type=ButtonType.route,
        name=getattr(t.values, key).name,
        description=getattr(t.values, key).description,
        buttons=[
            Btn(
                type=ButtonType.decimal,
                min=min_role_n,
                key=f'roles.{key}.n'
            ),
            Btn(
                type=ButtonType.toggle,
                key=f'roles.{key}.enable',
                options=[
                    Opt(
                        name=t.options.enable,
                        value=True
                    ),
                    Opt(
                        name=t.options.disable,
                        value=False
                    )
                ]
            )
        ]
    )


def get_settings_menu_config(t: Localization) -> MessageMenu:
    t = t.group.settings_menu
    return MessageMenu(
        description=t.description,
        buttons=[
            Btn(
                type=ButtonType.select,
                name=t.values.language.name,
                description=t.values.language.description,
                key='language',
                options=[Opt(name=tt.language, value=key) for key, tt in get_all_translations().items()]
            ),
            Btn(
                type=ButtonType.route,
                name=t.values.command_rights.name,
                description=t.values.command_rights.description,
                buttons=[command_route_button(t.values.command_rights, c) for c in
                         ('game', 'start', 'stop', 'extend', 'reduce')]
            ),
            Btn(
                type=ButtonType.route,
                name=t.values.time.name,
                description=t.values.time.description,
                buttons=[time_route_button(t.values.time.values, key) for key in
                         ('registration', 'extend', 'reduce', 'night', 'day', 'poll', 'vote')]
            ),
            Btn(
                type=ButtonType.route,
                name=t.values.players.name,
                description=t.values.players.description,
                buttons=[players_route_button(t.values.players.values, key) for key in ('max', 'min')]
            ),
            Btn(
                type=ButtonType.route,
                name=t.values.game.name,
                description=t.values.game.description,
                buttons=[game_toggle_button(t.values.game, key) for key in
                         ('start_at_night', 'mute_messages_from_dead', 'show_role_of_dead', 'show_role_of_departed',
                          'show_killer', 'allow_mafia_chat', 'show_night_actions', 'show_private_night_actions',
                          'last_words', 'commissioner_can_kill', 'lynching_confirmation')] + [
                            Btn(
                                type=ButtonType.route,
                                name=t.values.game.values.show_live_roles,
                                description=t.values.game.values.show_live_roles,
                                buttons=[Btn(
                                    type=ButtonType.toggle,
                                    key='game.show_live_roles',
                                    options=[
                                        Opt(
                                            name=t.values.game.options.enable,
                                            value='show'
                                        ),
                                        Opt(
                                            name=t.values.game.options.without_numbers,
                                            value='partially'
                                        ),
                                        Opt(
                                            name=t.values.game.options.disable,
                                            value='hide'
                                        )
                                    ]
                                )]
                            ),
                            Btn(
                                type=ButtonType.route,
                                name=t.values.game.values.show_message_on_vote,
                                description=t.values.game.values.show_message_on_vote,
                                buttons=[Btn(
                                    type=ButtonType.toggle,
                                    key='game.show_message_on_vote',
                                    options=[
                                        Opt(
                                            name=t.values.game.options.enable,
                                            value='show'
                                        ),
                                        Opt(
                                            name=t.values.game.options.anonymously,
                                            value='partially'
                                        ),
                                        Opt(
                                            name=t.values.game.options.disable,
                                            value='hide'
                                        )
                                    ]
                                )]
                            )
                        ]
            ),
            Btn(
                type=ButtonType.route,
                name=t.values.roles.name,
                description=t.values.roles.description,
                buttons=[
                            Btn(
                                type=ButtonType.route,
                                name=t.values.roles.values.maf.name,
                                description=t.values.roles.values.maf.description,
                                buttons=[Btn(
                                    type=ButtonType.decimal,
                                    key='roles.maf.n',
                                    min=min_role_n,
                                )]
                            )
                        ] + [role_route_button(t.values.roles, key) for key in
                             ('srg', 'doc', 'whr', 'scd', 'mnc', 'lwr', 'lck', 'bum')]
            ),
        ]
    )
