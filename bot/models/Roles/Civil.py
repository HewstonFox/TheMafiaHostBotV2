from random import choice

from aiohttp import ClientSession, ClientConnectorError

from bot.models.Roles.BaseRole import BaseRole
from bot.models.Roles.Incognito import Incognito
from bot.models.Roles.constants import Team
from config import env

__hack = BaseRole  # hack to avoid removing "unused" import which need for correct import sequence


class Civil(Incognito):
    shortcut = 'civ'
    team = Team.civ

    async def send_action(self):
        async with ClientSession() as session:
            while True:
                try:
                    response = await session.get(choice((env.RANDOM_CAT_API_URL, env.RANDOM_DOG_API_URL)))
                    data = await response.json()
                except ClientConnectorError:
                    continue
                image_url: str = data[0]['url']
                lower_image_url = image_url.lower()
                if not lower_image_url.endswith('webm'):
                    break

        if lower_image_url.endswith(('.jpg', '.jpeg', '.png')):
            await self.user.bot.send_photo(chat_id=self.user.id, photo=image_url)
        elif lower_image_url.endswith(('.gif', '.mpeg', '.mpg', '.h264')):
            await self.user.bot.send_animation(chat_id=self.user.id, animation=image_url)
        else:
            await self.user.bot.send_video(chat_id=self.user.id, video=image_url)
