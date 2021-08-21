from typing import Optional

from bot.controllers.ActionController.Actions.BaseAction import BaseAction, is_blocked
from bot.controllers.ActionController.Actions.KillAction import KillAction, IncognitoKillAction


class VoteAction(BaseAction):
    order = 5

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
