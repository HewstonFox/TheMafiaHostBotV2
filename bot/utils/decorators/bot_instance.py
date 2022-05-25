import traceback
from asyncio import sleep
from functools import wraps
from typing import Callable

from aiogram.utils.exceptions import Unauthorized, MessageToDeleteNotFound, MessageToReplyNotFound, RetryAfter, \
    MessageNotModified, InvalidQueryID, MessageToEditNotFound, UserIsAnAdministratorOfTheChat, CantRestrictChatOwner, \
    MethodIsNotAvailable, MessageToForwardNotFound, MessageIdInvalid, MessageToPinNotFound, MessageCantBeEdited, \
    MessageCantBeDeleted, MessageCantBeForwarded, ChatAdminRequired, NotEnoughRightsToPinMessage, \
    NotEnoughRightsToRestrict, MessageIsTooLong

from bot.constants import TELEGRAM_MESSAGE_MAX_SIZE
from bot.types import RetryBotBase
from bot.utils.shared import raise_if_error, batch_str
from config import env


def message_retry(func: Callable) -> Callable:
    """func(self, *args, **kwargs)"""

    @wraps(func)
    async def wrapper(self: RetryBotBase, *args, **kwargs):
        i = 0
        while i < self.repeat:
            try:
                return await func(self, *args, **kwargs)
            except (
                    MessageNotModified,
                    MessageToForwardNotFound,
                    MessageIdInvalid,
                    MessageToDeleteNotFound,
                    MessageToPinNotFound,
                    MessageToReplyNotFound,
                    MessageCantBeEdited,
                    MessageCantBeDeleted,
                    MessageCantBeForwarded,
                    MessageToEditNotFound,
                    InvalidQueryID,
                    ChatAdminRequired,
                    NotEnoughRightsToPinMessage,
                    NotEnoughRightsToRestrict,
                    MethodIsNotAvailable,
                    CantRestrictChatOwner,
                    UserIsAnAdministratorOfTheChat,
                    Unauthorized,
            ) as e:
                return e
            except RetryAfter as e:
                await sleep(e.timeout)
            except MessageIsTooLong as e:
                if 'text' in kwargs:
                    key = 'text'
                    message = kwargs['text']
                elif 'caption' in kwargs:
                    key = 'caption'
                    message = kwargs['caption']
                else:
                    for i, v in enumerate(args):
                        if type(v) == str and len(v) > TELEGRAM_MESSAGE_MAX_SIZE:
                            key = i
                            message = v
                            break
                    else:
                        key = None
                        message = None

                if message is None or key is None:
                    return e

                if 'chat_id' in kwargs:
                    chat_id = kwargs['chat_id']
                else:
                    chat_id = args[0]

                batched_message = batch_str(message, TELEGRAM_MESSAGE_MAX_SIZE)
                if type(key) == str:
                    kwargs[key] = batched_message[0]
                else:
                    args = args[:key] + tuple([batched_message[0]]) + args[key + 1:]

                res = await func(self, *args, **kwargs)
                for msg in batched_message[1:]:
                    await self.send_message(chat_id=chat_id, text=msg)
                return res

            except Exception as e:
                print(e)
                i += 1
                await sleep(1)
                if i == self.repeat:
                    return e

    return wrapper


def notify_error(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self: RetryBotBase, *args, **kwargs):
        try:
            result = await func(self, *args, **kwargs)
            raise_if_error(result)
            return result
        except (Unauthorized, TypeError) as e:
            return e
        except Exception as e:
            print(e)
            await self.send_message(env.NOTIFICATION_CHAT, f"Error:\n`{traceback.format_exc()}`")
            return e

    return wrapper


def soft_error(func: Callable) -> Callable:
    """func(*args, **kwargs)"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(e)
            return e

    return wrapper
