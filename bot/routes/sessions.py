import json

from aiohttp import web
from aiohttp.web_request import Request

from bot.controllers.SessionController.SessionController import SessionController
from bot.routes.helpers.decorators import with_auth

SessionsRoutes = web.RouteTableDef()


@SessionsRoutes.get('/sessions')
@with_auth
async def get_sessions_handler(request: Request):
    sessions = SessionController.get_active_sessions()
    sessions_json = f'[{",".join([session.json() for session in sessions.values()])}]'
    return web.Response(body=sessions_json, content_type='application/json;utf-8')


@SessionsRoutes.get('/sessions/{id}')
@with_auth
async def get_session_handler(request: Request):
    chat_id = request.match_info['id']
    if not chat_id:
        raise web.HTTPNotFound()
    session = SessionController.get_session(int(chat_id))
    if not session:
        raise web.HTTPNotFound()
    return web.Response(body=session.json(), content_type='application/json;utf-8')
