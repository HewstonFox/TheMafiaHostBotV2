from os import path
import urllib.parse
import json

from bot.controllers.SessionController.Session import Session
from config import env


def create_error_link(traceback: str):
    with open(path.join('assets', 'templates', 'error_template.html')) as f:
        content = f.read().replace('  ', ' ').replace('\n', '').replace('\t', '')
    content = content.replace('#error', traceback)
    return env.ERROR_PAGE_ROOT + '#data:text/html,' + urllib.parse.quote(content)


def create_session_link(session: Session):
    with open(path.join('assets', 'templates', 'session_template.html')) as f:
        content = f.read().replace('  ', ' ').replace('\n', '').replace('\t', '')
    content = content.replace('#session', json.dumps(session.get_dump(), indent=2, default=lambda x: x.get_dump()))
    return env.ERROR_PAGE_ROOT + '#data:text/html,' + urllib.parse.quote(content)
