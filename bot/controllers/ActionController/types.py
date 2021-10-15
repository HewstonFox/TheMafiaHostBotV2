from enum import Enum


class VoteFailReason(Enum):
    no_votes = 'no_votes'
    too_much_candidates = 'too_much_candidates'
    no_fails = 'no_fails'
