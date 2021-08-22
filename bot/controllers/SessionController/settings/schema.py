from schema import Schema, Or, And

from bot.localization import get_all_translations
from bot.utils.schema import field_range
from bot.controllers.SessionController.settings.constants import *

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
        'registration': And(Or(int, float), field_range(registration_min)),
        'extend': And(Or(int, float), field_range(registration_change_time_min)),
        'reduce': And(Or(int, float), field_range(registration_change_time_min)),
        'night': And(Or(int, float), field_range(night_min)),
        'day': And(Or(int, float), field_range(day_min)),
        'poll': And(Or(int, float), field_range(poll_min)),
        'vote': And(Or(int, float), field_range(vote_min)),  #
    },
    'players': {
        'max': And(int, field_range(min_players)),
        'min': And(int, field_range(min_players)),
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
        'show_live_roles': Or(*DisplayType.values()),
        'show_message_on_vote': Or(*DisplayType.values()),
    },
    'roles': {
        'maf': {
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'scd': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'whr': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'doc': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'shr': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'lwr': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'lck': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'mnc': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
        'bum': {
            'enable': bool,
            'n': And(Or(int, float), field_range(min_role_n))
        },
    }
})
