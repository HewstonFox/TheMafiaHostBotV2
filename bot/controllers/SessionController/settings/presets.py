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
            'extend_default': 30,
            'reduce_default': 30,
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
                'n': 8.0
            },
            'shr': {
                'enable': True,
                'n': 8.5
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
