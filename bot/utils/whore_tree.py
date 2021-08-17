from aiogram.types import User


class WhoreTree:
    def __init__(self, fucker: User):
        self.fucker = fucker
        self.fuckers: list['WhoreTree'] = []

    def is_fucked(self, prev_fuckers: list['WhoreTree'] = []):
        if self in prev_fuckers:
            return True
        return any([not fucker.is_fucked(prev_fuckers + [self]) for fucker in self.fuckers])


def create_whore_tree(action, actions: list, checked: list[User] = []):
    fucks = [act for act in actions if act.is_blocker]

    fucker = WhoreTree(action.actor)

    if fucker.fucker not in checked:
        fucker.fuckers = [
            create_whore_tree(fuck, fucks, checked + [fucker.fucker])
            for fuck in fucks if fuck.target == action.actor
        ]

    return fucker
