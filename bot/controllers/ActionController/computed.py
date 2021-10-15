from bot.controllers.ActionController.Actions.VoteAction import VoteAction

vote_types = [item for sub in VoteAction.__subclasses__() for item in sub.__subclasses__()]
