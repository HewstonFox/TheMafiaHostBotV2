from aiogram.types import User

from bot.controllers.ActionController.Actions.BlockAction import BlockAction
from bot.controllers.ActionController.Actions.CureAction import CureAction
from bot.controllers.SessionController.Session import Session
from bot.models.Roles import BaseRole
from bot.utils.whore_tree import create_whore_tree

session = Session(chat_id=-1)

mia = BaseRole(User(first_name='mia'), session)
agata = BaseRole(User(first_name='agata'), session)
adam = BaseRole(User(first_name='adam'), session)
bill = BaseRole(User(first_name='bill'), session)
cortana = BaseRole(User(first_name='cortana'), session)
sebastian = BaseRole(User(first_name='sebastian'), session)

actions = [
    BlockAction(mia, sebastian),
    BlockAction(sebastian, adam),
    CureAction(adam, cortana),
    BlockAction(cortana, agata),
    BlockAction(agata, bill),
    BlockAction(bill, mia),
]

if __name__ == '__main__':
    for action in actions:
        print(action.actor.user.first_name, create_whore_tree(action, actions).is_fucked())
