from bot.controllers.SessionController.Session import Session
from bot.types import ResultConfig


def get_result_config(session: Session) -> ResultConfig:
    config = {
        'alive': [],
        'dead': [],
        'winners': [],
        'losers': [],
        'alive_roles': {}
    }
    for player in session.roles.values():
        config['winners' if player.won else 'losers'].append(player)
        config['alive' if player.alive else 'dead'].append(player)
        if not player.alive:
            continue
        if player.shortcut not in config['alive_roles']:
            config['alive_roles'][player.shortcut] = 0
        config['alive_roles'][player.shortcut] += 1

    return config
