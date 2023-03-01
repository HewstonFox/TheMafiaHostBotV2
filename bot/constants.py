from config import env
import sys

WEBHOOK_PATH = f'/webhook/{env.BOT_TOKEN}'
WEBAPP_HOST = '0.0.0.0'

ARGS_LEN = len(sys.argv)
WEBAPP_PORT = sys.argv[1] if ARGS_LEN > 1 else env.PORT
WEBHOOK_HOST = sys.argv[2] if ARGS_LEN > 2 else env.BASE_URI
IS_WEBHOOK = WEBAPP_PORT and WEBHOOK_HOST
IS_PING_PONG = IS_WEBHOOK and bool(
    env.PING_PONG) and env.PING_PONG.lower() == 'true'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}' if IS_WEBHOOK else None

TELEGRAM_MESSAGE_MAX_SIZE = 4096

RANDOM_CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
RANDOM_DOG_API_URL = "https://api.thedogapi.com/v1/images/search"

IMAGE_AUTHOR_HTML_LINK = "<a href='https://www.deviantart.com/cybercinnamonroll'>cybercinnamonroll</a>"
COOKIE_KEY = "the_mafia_host_bot_token"
