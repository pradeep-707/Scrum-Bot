from dotenv import dotenv_values
import os

_dir_path = os.path.dirname(os.path.realpath(__file__))
_path = _dir_path + "/.env"
config = dotenv_values(_path)


BOT_TOKEN = config.get("BOT_TOKEN") if config.get("BOT_TOKEN") else "TOKEN"
BASE_URL = config.get("BASE_URL") if config.get(
    "BASE_URL") else "http://127.0.0.1:8000/"
