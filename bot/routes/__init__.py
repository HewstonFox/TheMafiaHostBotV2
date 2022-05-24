from aiohttp.web_app import Application

from bot.routes.auth import AuthRoutes
from bot.routes.app import AppRoutes
from bot.routes.errors import ErrorsRoutes
from bot.routes.sessions import SessionsRoutes


def apply(web_app: Application) -> Application:
    web_app.add_routes(AppRoutes)
    web_app.add_routes(AuthRoutes)
    web_app.add_routes(SessionsRoutes)
    web_app.add_routes(ErrorsRoutes)
    return web_app
