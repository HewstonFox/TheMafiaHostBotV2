from bot.controllers.MenuController.types import ButtonType
from bot.localization import Localization, get_all_translations


def get_settings_menu_config(t: Localization):
    t = t.group.settings_menu
    return {
        'description': t.description,
        'buttons': [
            {
                'type': ButtonType.select,
                'name': t.values.language.name,
                'description': t.values.language.description,
                'path': 'language',
                'buttons': list(map(
                    lambda translation: {
                        'name': translation[1].language,
                        'value': translation[0]
                    },
                    get_all_translations().items())
                )
            }
        ]
    }
