from os import environ
import logging

# general
PROJECT_NAME=environ.get("PROJECT_NAME") \
            if environ.get("PROJECT_NAME") \
            else "Scrum_Bot"

DEBUG= True if environ.get("DEBUG") and environ.get("DEBUG") == "DEBUG" \
            else False

# database
MONGO_URI = environ.get("MONGO_URI") \
            if environ.get("MONGO_URI") \
            else "mongodb://127.0.0.1:27017/ScrumBot"

#jwt
JWT_ALGORITHM = environ.get("JWT_ALGORITHM") \
            if environ.get("JWT_ALGORITHM") \
            else "HS256"

JWT_SECRET = environ.get("JWT_SECRET")

JWT_EXPIRE_TIME = int(environ.get("JWT_EXPIRE_TIME")) \
            if (environ.get("JWT_EXPIRE_TIME")) \
            else 0



# Auth Headers
AUTH_HEADER_KEY = environ.get("HEADER_KEY") \
            if environ.get("HEADER_KEY") \
            else "Authorization"

JWT_TOKEN_PREFIX = environ.get("JWT_TOKEN_PREFIX") \
            if environ.get("JWT_TOKEN_PREFIX") \
            else "Bearer"

# Bot Headers
BOT_HEADER_KEY=environ.get("BOT_HEADER_KEY") \
            if environ.get("BOT_HEADER_KEY") \
            else "secure-bot-secret"

BOT_TOKEN_PREFIX=environ.get("BOT_TOKEN_PREFIX")

# logging
LOGGING_LEVEL=logging.DEBUG if DEBUG else logging.INFO
