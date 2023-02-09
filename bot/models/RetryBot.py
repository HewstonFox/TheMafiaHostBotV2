from bot.types import RetryBotBase
from bot.utils.decorators.bot_instance import message_retry, soft_error


class RetryBot(RetryBotBase):
    def __init__(self, *args, **kwargs):
        super(RetryBot, self).__init__(*args, **kwargs)
        self.repeat = 5

    @message_retry
    async def send_message(self, *args, **kwargs):
        return await super(RetryBot, self).send_message(*args, **kwargs)

    @message_retry
    async def send_photo(self, *args, **kwargs):
        return await super(RetryBot, self).send_photo(*args, **kwargs)

    @message_retry
    async def send_animation(self, *args, **kwargs):
        return await super(RetryBot, self).send_animation(*args, **kwargs)

    @message_retry
    async def send_video(self, *args, **kwargs):
        return await super(RetryBot, self).send_video(*args, **kwargs)

    @message_retry
    async def edit_message_reply_markup(self, *args, **kwargs):
        return await super(RetryBot, self).edit_message_reply_markup(*args, **kwargs)

    @message_retry
    async def edit_message_text(self, *args, **kwargs):
        return await super(RetryBot, self).edit_message_text(*args, **kwargs)

    @message_retry
    async def answer_callback_query(self, *args, **kwargs):
        return await super(RetryBot, self).answer_callback_query(*args, **kwargs)

    @soft_error
    async def pin_chat_message(self, *args, **kwargs):
        return await super(RetryBot, self).pin_chat_message(*args, **kwargs)

    @soft_error
    async def unpin_chat_message(self, *args, **kwargs):
        return await super(RetryBot, self).unpin_chat_message(*args, **kwargs)

    @soft_error
    async def delete_message(self, *args, **kwargs):
        return await super(RetryBot, self).delete_message(*args, **kwargs)

    @message_retry
    async def restrict_chat_member(self, *args, **kwargs):
        return await super(RetryBot, self).restrict_chat_member(*args, **kwargs)

    @message_retry
    async def export_chat_invite_link(self, *args, **kwargs):
        return await super(RetryBot, self).export_chat_invite_link(*args, **kwargs)

    @message_retry
    async def create_chat_invite_link(self, *args, **kwargs):
        return await super(RetryBot, self).create_chat_invite_link(*args, **kwargs)

    @message_retry
    async def revoke_chat_invite_link(self, *args, **kwargs):
        return await super(RetryBot, self).revoke_chat_invite_link(*args, **kwargs)

    @message_retry
    async def edit_chat_invite_link(self, *args, **kwargs):
        return await super(RetryBot, self).edit_chat_invite_link(*args, **kwargs)

    @message_retry
    async def get_chat_administrators(self, *args, **kwargs):
        return await super(RetryBot, self).get_chat_administrators(*args, **kwargs)
