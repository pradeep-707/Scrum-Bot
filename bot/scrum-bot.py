import discord
import re
from discord.ext import commands
from database_requests import *
from reactions import Reactions
from config import BOT_TOKEN

bot = commands.Bot(command_prefix='!')


def get_keywords_and_content(message: str) -> tuple[list[str], str]:
    pattern = re.compile(r'!scrum(?P<keywords>[^:]+):(?P<content>[\w\W]+)')
    result = pattern.match(message)
    if not result:
        return None, None
    d = result.groupdict()
    keywords = [keyword.strip()
                for keyword in d['keywords'].split(',') if keyword.strip() != '']
    content = d['content'].strip()
    return keywords, content


async def handle_reply(message: discord.Message, parent_message_id: int):
    success = await add_reply(message.id, message.content, f'{message.author.name}#{message.author.discriminator}', parent_message_id)
    if success:
        await message.add_reaction(Reactions.THUMBS_UP.value)
    else:
        await message.add_reaction(Reactions.F.value)


@bot.command(brief='', description='')
async def scrumstart(ctx: commands.Context):
    await ctx.send(await start_scrum())


@bot.command(brief='', description='')
async def scrumend(ctx: commands.Context):
    await ctx.send(await end_scrum())


@bot.command(brief='', description='')
async def scrum(ctx: commands.Context):
    message: discord.Message = ctx.message
    keywords, content = get_keywords_and_content(message.content)
    if not keywords or not content:
        await message.add_reaction(Reactions.THUMBS_DOWN.value)
        return
    if await add_scrum_entry(message.id, content, f'{ctx.author.name}#{ctx.author.discriminator}', keywords):
        await message.add_reaction(Reactions.THUMBS_UP.value)
    else:
        await message.add_reaction(Reactions.F.value)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    for reaction in after.reactions:
        await reaction.remove(bot.user)
    if after.content.startswith('!scrum '):
        keywords, content = get_keywords_and_content(after.content)
        if not keywords or not content:
            await after.add_reaction(Reactions.THUMBS_DOWN.value)
            return
        success = await update_message(after.id, content, keywords)
        if not success:
            await bot.process_commands(after)
        else:
            await after.add_reaction(Reactions.THUMBS_UP.value)
    else:
        if await update_message(after.id, after.content):
            await after.add_reaction(Reactions.THUMBS_UP.value)


@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)
    reference: discord.MessageReference = message.reference
    if message.reference and not message.content.startswith('!scrum'):
        parent_message_id = reference.message_id
        await handle_reply(message, parent_message_id)


@bot.event
async def on_message_delete(message: discord.Message):
    await delete_message(message.id)


@bot.event
async def on_ready():
    print("ready!")

bot.run(BOT_TOKEN)
