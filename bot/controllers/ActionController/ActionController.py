from typing import Dict, Type, Optional, Union

from bot.controllers import BaseController
from bot.controllers.ActionController.types import VoteFailReason
from bot.models.Roles import BaseRole
from bot.controllers.ActionController.Actions.BaseAction import BaseAction
from bot.controllers.ActionController.Actions.VoteAction import VoteAction
from bot.types import ChatId
from bot.utils.shared import count_bases_depth
from bot.controllers.ActionController.computed import vote_types


class ActionController(BaseController):

    @classmethod
    async def apply_actions(cls, players: Dict[ChatId, BaseRole]) -> dict[VoteAction, Union[VoteFailReason, BaseRole]]:
        actions = sorted([player.action for player in players.values() if player.action], key=lambda x: x.order)

        resolved_votes, vote_fails_reasons = await cls.resole_votes(
            [vote for vote in actions if isinstance(vote, VoteAction)])

        actions = [act for act in actions if not isinstance(act, VoteAction)] + resolved_votes

        for action in actions:
            await action.apply()

        for player in players.values():
            player.action = None

        return vote_fails_reasons

    @classmethod
    async def resole_votes(cls, _votes: list[VoteAction]) \
            -> tuple[list[BaseAction], dict[VoteAction, Optional[VoteFailReason]]]:
        votes = [vote for vote in _votes if await vote.apply()]
        vote_results = {vote_type: VoteFailReason.nothing for vote_type in vote_types}

        votes_config = {
            vote_type: cls.attach_role_priority(vote_type, [vote for vote in votes if isinstance(vote, vote_type)])
            for vote_type in vote_types
        }

        result_actions: list[BaseAction] = []

        for key, votes in votes_config.items():
            if not len(votes.keys()):
                continue
            actor = votes[max(votes.keys())][0].actor
            action = key.get_result_action()
            targets = {}

            for factor, row_votes in votes.items():
                for vote in row_votes:
                    if vote.target.user.id not in targets:
                        targets[vote.target.user.id] = [0, vote.target]
                    targets[vote.target.user.id][0] += factor
            if len(targets.values()):
                max_votes = max(targets.values(), key=lambda x: x[0])
                if len([vote for vote in targets.values() if vote[0] == max_votes[0]]) > 1:
                    vote_results[key] = VoteFailReason.both
                    continue
                result_actions.append(action(actor, max_votes[1]))
                vote_results[key] = max_votes[1]
        return result_actions, vote_results

    @classmethod
    def attach_role_priority(cls, vote_type: Type[VoteAction], votes: list[VoteAction]) -> Dict[int, list[VoteAction]]:
        base_delta = count_bases_depth(vote_type) - 1
        types_set = set([type(vote) for vote in votes])
        return {
            count_bases_depth(vote_subtype) - base_delta:
                [vote for vote in votes if type(vote) == vote_subtype]
            for vote_subtype in types_set
        }
