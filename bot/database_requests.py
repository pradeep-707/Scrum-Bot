import aiohttp
from config import BASE_URL, BOT_HEADER_KEY, BOT_TOKEN_PREFIX, BOT_SECRET_TOKEN

headers = {
    BOT_HEADER_KEY: f"{BOT_TOKEN_PREFIX} {BOT_SECRET_TOKEN}"
}

async def start_scrum() -> str:
    GET_URL = BASE_URL + "bot/scrum/start"
    async with aiohttp.ClientSession() as session:
        async with session.get(GET_URL, headers=headers) as response:
            response_body = await response.json()
            if response.status >= 400:
                return response_body["detail"]["message"]
            return response_body["message"]


async def end_scrum() -> str:
    GET_URL = BASE_URL + "bot/scrum/end"
    async with aiohttp.ClientSession() as session:
        async with session.get(GET_URL, headers=headers) as response:
            response_body = await response.json()
            if response.status >= 400:
                return response_body["detail"]["message"]
            return response_body["message"]


async def add_scrum_entry(message_id, message, author, tags) -> bool:
    POST_URL = BASE_URL + "bot/message"
    scrum_entry = {
        "messageId": message_id,
        "message": message,
        "author": author,
        "tags": tags,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(POST_URL, json=scrum_entry, headers=headers) as response:
            if response.status >= 400:
                return False
            response_body = await response.json()
            return response_body['code'] == 200


async def add_reply(message_id, content, author, parent_message_id) -> bool:
    POST_URL = BASE_URL + "bot/message"
    add_reply_body = {
        "messageId": message_id,
        "message": content,
        "author": author,
        "isReply": True,
        "parentMessage": parent_message_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(POST_URL, json=add_reply_body, headers=headers) as response:
            if response.status >= 400:
                return False
            response_body = await response.json()
            return response_body['code'] == 200


async def delete_message(message_id) -> bool:
    DELETE_URL = BASE_URL + "bot/message"
    async with aiohttp.ClientSession() as session:
        async with session.delete(DELETE_URL, json={'messageId': message_id}, headers=headers) as response:
            if response.status >= 400:
                return False
            response_body = await response.json()
            return response_body['code'] == 200


async def update_message(message_id, content, tags=None) -> bool:
    PUT_URL = BASE_URL + "bot/message"
    update_message_body = {
        "messageId": message_id,
        "message": content
    }
    if tags:
        update_message_body["tags"] = tags
    async with aiohttp.ClientSession() as session:
        async with session.put(PUT_URL, json=update_message_body, headers=headers) as response:
            if response.status >= 400:
                return False
            response_body = await response.json()
            return response_body['code'] == 200
