# __main__
import os
from typing import Tuple
import discord
import logging

import handler.functions
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

TOKEN = os.getenv("COMPENT_DISCORD_TOKEN", "")
if not TOKEN:
    logger.error("Missing DISCORD_TOKEN environment variable.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def split_content(msg: discord.Message) -> Tuple[str, str]:
    content = msg.content
    if not content:
        return "", ""
    split_content = msg.content.split()
    return split_content[0], split_content[1:]


@client.event
async def on_ready() -> None:
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    logger.info(f"Message from {message.author} (ID: {message.author.id})")
    command = message.content.split()[0].strip().lower()
    if command == "!quote":
        await handler.functions.handle_quote(message)


client.run(TOKEN)
