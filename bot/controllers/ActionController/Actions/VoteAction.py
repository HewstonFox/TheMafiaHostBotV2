from typing import Optional

from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked
from bot.controllers.ActionController.Actions.KillAction import KillAction, IncognitoKillAction
from bot.models.Roles import BaseRole


class VoteAction(BaseAction):
    order = 5

    def __init__(self, actor: 'BaseRole', target: 'BaseRole'):
        super().__init__(actor, target)

    @is_blocked
    async def apply(self) -> Optional[bool]:
        return True

    @classmethod
    def get_result_action(cls):
        raise NotImplementedError


class KillVoteAction(VoteAction):
    @classmethod
    def get_result_action(cls):
        return KillAction


class IncognitoKillVoteAction(VoteAction):
    @classmethod
    def get_result_action(cls):
        return IncognitoKillAction


class DayKillVoteAction(IncognitoKillVoteAction):
    pass


class MafiaKillVoteAction(KillVoteAction):
    pass


class DonKillVoteAction(MafiaKillVoteAction):
    pass
