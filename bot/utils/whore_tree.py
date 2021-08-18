from aiogram.types import User


class WhoreTree:
    def __init__(self, fucker: User):
        self.fucker = fucker
        self.fuckers: list['WhoreTree'] = []

    def is_fucked(self, prev_fuckers: list['WhoreTree'] = []) -> bool:
        if self in prev_fuckers:
            return not not len(prev_fuckers) % 2
        return any([not fucker.is_fucked(prev_fuckers + [self]) for fucker in self.fuckers])


def create_whore_tree(action, actions: list, checked: list[WhoreTree] = []):
    fucks = [act for act in actions if act.is_blocker]

    if len(fucker := [ch for ch in checked if ch.fucker == action.actor]):
        return fucker[0]

    fucker = WhoreTree(action.actor)
    fucker.fuckers = [
        create_whore_tree(fuck, fucks, checked + [fucker])
        for fuck in fucks if fuck.target == action.actor
    ]

    return fucker
