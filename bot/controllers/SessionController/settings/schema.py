from schema import Schema, Or

from bot.localization import get_all_translations

settings_schema = Schema({
    'language': Or(*get_all_translations()),
    'command_rights': {
        'game': bool,
        'start': bool,
        'stop': bool,
        'extend': bool,
        'reduce': bool
    },
    'time': {
        'registration': Or(int, float),
        'extend': Or(int, float),
        'reduce': Or(int, float),
        'night': Or(int, float),
        'day': Or(int, float),
        'poll': Or(int, float),
        'vote': Or(int, float),
    },
    'players': {
        'max': int,
        'min': int
    },
    'game': {
        'start_at_night': bool,
        'mute_messages_from_dead': bool,
        'show_role_of_dead': bool,
        'show_role_of_departed': bool,
        'show_killer': bool,
        'allow_mafia_chat': bool,
        'show_night_actions': bool,
        'show_private_night_actions': bool,
        'last_words': bool,
        'commissioner_can_kill': bool,
        'show_live_roles': Or('show', 'partially', 'hide'),
        'show_message_on_vote': Or('show', 'partially', 'hide'),
    },
    'roles': {
        'maf': {
            'n': Or(int, float)
        },
        'scd': {
            'enable': bool,
            'n': Or(int, float)
        },
        'whr': {
            'enable': bool,
            'n': Or(int, float)
        },
        'doc': {
            'enable': bool,
            'n': Or(int, float)
        },
        'shr': {
            'enable': bool,
            'n': Or(int, float)
        },
    }
})
