# __main__
from typing import Tuple
import discord
import logging

import handler.function
import utils.logging as lg
from utils import general
from handler.settings import LOADED_TOKENS, load_tokens

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None: 
    logger.info(f"Logged in as {client.user} (ID: {client.user.id})")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    
    logger.info(f"Message from {message.author} (ID: {message.author.id})")
    command, _ = general.split_first_token(message.content)
    await handler.function.handle_command(command, message)

if __name__ == "__main__":
    load_tokens()
    client.run(LOADED_TOKENS.get("COMPEND_DISCORD_TOKEN"))
