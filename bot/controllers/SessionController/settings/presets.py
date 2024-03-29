class SettingsPreset:
    default = {
        'command_rights': {
            'game': False,
            'start': False,
            'stop': False,
            'extend': False,
            'reduce': False
        },
        'time': {
            'registration': 600,
            'extend': 30,
            'reduce': 30,
            'night': 60,
            'day': 300,
            'poll': 60,
            'vote': 30,
        },
        'players': {
            'max': 21,
            'min': 4
        },
        'game': {
            'start_at_night': True,
            'mute_messages_from_dead': True,
            'show_role_of_dead': True,
            'show_role_of_departed': True,
            'show_killer': True,
            'allow_mafia_chat': True,
            'show_night_actions': True,
            'show_private_night_actions': True,
            'last_words': True,
            'commissioner_can_kill': True,
            'lynching_confirmation': True,
            'show_live_roles': 'show',  # 'show', 'hide', 'partially'
            'show_message_on_vote': 'show',  # 'show', 'hide', 'partially'
        },
        'roles': {
            'maf': {
                'n': 4.0
            },
            'scd': {
                'enable': True,
                'n': 12.1
            },
            'whr': {
                'enable': True,
                'n': 10.1
            },
            'doc': {
                'enable': True,
                'n': 13
            },
            'srg': {
                'enable': True,
                'n': 8
            },
            'lwr': {
                'enable': True,
                'n': 15
            },
            'lck': {
                'enable': True,
                'n': 15
            },
            'mnc': {
                'enable': True,
                'n': 15
            },
            'bum': {
                'enable': True,
                'n': 15
            },
        }
    }

    silent = {
        'game': {
            'mute_messages_from_dead': True,
            'show_role_of_dead': False,
            'show_role_of_departed': False,
            'show_killer': False,
            'show_night_actions': False,
            'show_private_night_actions': False,
            'show_live_roles': 'hide',
            'show_message_on_vote': 'hide',
        },
    }

    classic = {
        'time': {
            'night': 60,
            'day': 600,
            'poll': 60,
            'vote': 30,
        },
        'players': {
            'max': 10,
            'min': 10
        },
        'game': {
            'start_at_night': True,
            'mute_messages_from_dead': True,
            'show_role_of_dead': False,
            'show_killer': False,
            'allow_mafia_chat': True,
            'show_night_actions': False,
            'show_private_night_actions': True,
            'last_words': True,
            'commissioner_can_kill': False,
            'show_live_roles': 'hide',  # 'show', 'hide', 'partially'
            'show_message_on_vote': 'show',  # 'show', 'hide', 'partially'
        },
        'roles': {
            'maf': {
                'n': 4.0
            },
            'srg': {
                'enable': True,
                'n': 8.5
            },
            'scd': {
                'enable': False,
            },
            'whr': {
                'enable': False,
            },
            'doc': {
                'enable': False,
            },
            'lwr': {
                'enable': False
            },
            'lck': {
                'enable': False
            },
            'mnc': {
                'enable': False
            },
            'bum': {
                'enable': False
            },
        }
    }
