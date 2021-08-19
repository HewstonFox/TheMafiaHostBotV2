from typing import Dict, Type

from bot.controllers import BaseController
from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.VoteAction import VoteAction
from bot.models.Roles import BaseRole
from bot.types import ChatId
from bot.utils.shared import count_bases_depth


class ActionController(BaseController):

    @classmethod
    async def apply_actions(cls, players: Dict[ChatId, BaseRole]):
        actions = sorted([player.action for player in players.values()], key=lambda x: x.order)

        resolved_votes = cls.resole_votes([vote for vote in actions if isinstance(vote, VoteAction)])
        actions = [act for act in actions if not isinstance(act, VoteAction)] + resolved_votes

        for action in actions:
            await action.apply()

    @classmethod
    def resole_votes(cls, _votes: list[VoteAction]) -> list[BaseAction]:
        votes = [vote for vote in _votes if vote.apply()]
        vote_types = [item for sub in VoteAction.__subclasses__() for item in sub.__subclasses__()]
        #  creating of vote config with vote`s priority
        votes_config = {
            vote_type: cls.attach_role_priority(vote_type, [vote for vote in votes if isinstance(vote, vote_type)])
            for vote_type in vote_types
        }
        result_actions: list[BaseAction] = []
        for key, votes in votes_config.items():
            actor = votes[max(votes.keys())][0].actor
            action = key.get_result_action()
            targets = {}
            # Counting votes
            for factor, row_votes in votes.items():
                for vote in row_votes:
                    if vote.target.user.id not in targets:
                        targets[vote.target.user.id] = [0, vote.target]
                    targets[vote.target.user.id][0] += factor
            result_actions.append(action(actor, max(targets.values(), key=lambda x: x[0])[1]))
        return result_actions

    @classmethod
    def attach_role_priority(cls, vote_type: Type[VoteAction], votes: list[VoteAction]) -> Dict[int, list[VoteAction]]:
        base_delta = count_bases_depth(vote_type) - 1
        types_set = set([type(vote) for vote in votes])
        return {
            count_bases_depth(vote_subtype) - base_delta:
                [vote for vote in votes if type(vote) == vote_subtype]
            for vote_subtype in types_set
        }
