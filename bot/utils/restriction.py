from typing import Optional, Union
import datetime

from aiogram import Bot
from aiogram.types import ChatMemberStatus, ChatMember, ChatPermissions

from bot.types import ChatId
from aiogram.types.chat_member import ChatMemberRestricted

CHAT_MEMBER_RESTRICTIONS_LIST = [k for k in ChatMemberRestricted.__dict__ if k.startswith('can')]
SEND_RESTRICTIONS = {k: False for k in CHAT_MEMBER_RESTRICTIONS_LIST if k.startswith('can_send')}


def collect_permissions(member: ChatMember) -> Optional[dict[str, bool]]:
    if member.status == ChatMemberStatus.MEMBER:
        current_permissions = {k: True for k in CHAT_MEMBER_RESTRICTIONS_LIST}
    elif member.status == ChatMemberStatus.RESTRICTED:
        current_permissions = {}
        for permission in CHAT_MEMBER_RESTRICTIONS_LIST:
            current_permissions[permission] = getattr(member, permission)
    else:
        return
    return current_permissions


async def restriction_with_prev_state(
        bot: Bot,
        chat_id: ChatId,
        user_id: ChatId,
        restrictions: dict[str, bool],
        until_date: Union[int, datetime.datetime, datetime.timedelta, None] = None
) -> Optional[dict[str, bool]]:
    member = await bot.get_chat_member(chat_id, user_id)
    prev_permissions = collect_permissions(member)
    if not prev_permissions:
        return

    await bot.restrict_chat_member(
        chat_id,
        user_id,
        ChatPermissions(**restrictions),
        until_date
    )

    return prev_permissions
