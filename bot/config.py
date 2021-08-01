from dotenv import dotenv_values
import os

_dir_path = os.path.dirname(os.path.realpath(__file__))
_path = _dir_path + "/.env"
config = dotenv_values(_path)


BOT_TOKEN = config.get("BOT_TOKEN") if config.get("BOT_TOKEN") else "TOKEN"
BASE_URL = config.get("BASE_URL") if config.get(
    "BASE_URL") else "http://127.0.0.1:8000/"
BOT_HEADER_KEY = config.get("BOT_HEADER_KEY") if config.get(
    "BOT_HEADER_KEY") else "bot-secure-secret"
BOT_TOKEN_PREFIX = config.get("BOT_TOKEN_PREFIX") if config.get(
    "BOT_TOKEN_PREFIX") else "random_prefix"
BOT_SECRET_TOKEN = config.get("BOT_SECRET_TOKEN") if config.get(
    "BOT_SECRET_TOKEN") else "secure_secret"
