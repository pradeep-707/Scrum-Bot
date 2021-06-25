import logging
import os

from dotenv import dotenv_values

_dir_path = os.path.dirname(os.path.realpath(__file__))
_path = _dir_path + "/../.env"
config = dotenv_values(_path)

# general
PROJECT_NAME=config.get("PROJECT_NAME") \
            if config.get("PROJECT_NAME") \
            else "Scrum_Bot"

DEBUG= True if config.get("DEBUG") and config.get("DEBUG") == "DEBUG" \
            else False

# database
MONGO_URI = config.get("MONGO_URI") \
            if config.get("MONGO_URI") \
            else "mongodb://127.0.0.1:27017/ScrumBot"

#jwt
JWT_ALGORITHM = config.get("JWT_ALGORITHM") \
            if config.get("JWT_ALGORITHM") \
            else "HS256"

JWT_SECRET = config.get("JWT_SECRET")

JWT_EXPIRE_TIME = int(config.get("JWT_EXPIRE_TIME")) \
            if (config.get("JWT_EXPIRE_TIME")) \
            else 0



# Auth Headers
AUTH_HEADER_KEY = config.get("HEADER_KEY") \
            if config.get("HEADER_KEY") \
            else "Authorization"

JWT_TOKEN_PREFIX = config.get("JWT_TOKEN_PREFIX") \
            if config.get("JWT_TOKEN_PREFIX") \
            else "Bearer"

# Bot Headers
BOT_HEADER_KEY=config.get("BOT_HEADER_KEY") \
            if config.get("BOT_HEADER_KEY") \
            else "secure-bot-secret"

BOT_TOKEN_PREFIX=config.get("BOT_TOKEN_PREFIX")

# logging
LOGGING_LEVEL=logging.DEBUG if DEBUG else logging.INFO

CONSTANTS=config.get("CONSTANTS").split("|")[:-1]
CONSTANT_DEFAULT_VALUES=config.get("CONSTANT_DEFAULT_VALUES").split("|")[:-1]