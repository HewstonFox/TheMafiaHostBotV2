from config import env
import sys

WEBHOOK_PATH = f'/webhook/{env.BOT_TOKEN}'
WEBAPP_HOST = '0.0.0.0'

ARGS_LEN = len(sys.argv)
WEBAPP_PORT = sys.argv[1] if ARGS_LEN > 1 else env.PORT
WEBHOOK_HOST = sys.argv[2] if ARGS_LEN > 2 else env.BASE_URI
IS_WEBHOOK = WEBAPP_PORT and WEBHOOK_HOST
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}' if IS_WEBHOOK else None

TELEGRAM_MESSAGE_MAX_SIZE = 4096
