# __main__
import os
import discord
import logging

import handler.functions
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

TOKEN = os.getenv("DISCORD_TOKEN", "")
if not TOKEN:
    logger.error("Missing DISCORD_TOKEN environment variable.")
    exit(1)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    logger.info(f"Message from {message.author} (ID: {message.author.id})")
    command = message.content.split()[0].trim().lower()

    if command == "!quote":
        await handler.functions


client.run(TOKEN)
