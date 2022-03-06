import asyncio

from aiogram import Dispatcher
from aiogram.types import BotCommand, BotCommandScopeType, BotCommandScope

from bot.localization import Localization, get_default_translation, get_all_translations


def get_user_commands_list(t: Localization):
    return [
        BotCommand('start', t.commands.private.start),
        BotCommand('help', t.commands.private.help)
    ]


def get_group_commands_list(t: Localization):
    return [
        BotCommand('start', t.commands.group.start),
        BotCommand('help', t.commands.group.help),
        BotCommand('game', t.commands.group.game),
        BotCommand('extend', t.commands.group.extend),
        BotCommand('reduce', t.commands.group.reduce),
        BotCommand('leave', t.commands.group.leave),
        BotCommand('stop', t.commands.group.stop),
        BotCommand('settings', t.commands.group.settings),
    ]


AllPrivateChats = BotCommandScope.from_type(str(BotCommandScopeType.ALL_PRIVATE_CHATS))
AllGroupChats = BotCommandScope.from_type(str(BotCommandScopeType.ALL_GROUP_CHATS))


async def set_commands_list(dp: Dispatcher):
    bot = dp.bot
    default_t = get_default_translation()
    asyncio.create_task(bot.set_my_commands(get_user_commands_list(default_t), AllPrivateChats))
    asyncio.create_task(bot.set_my_commands(get_group_commands_list(default_t), AllGroupChats))

    for locale, t in get_all_translations().items():
        asyncio.create_task(
            bot.set_my_commands(get_user_commands_list(t), AllPrivateChats, locale))
        asyncio.create_task(
            bot.set_my_commands(get_group_commands_list(t), AllGroupChats, locale))
