# __main__
from typing import Tuple
import discord
from discord.ext import commands
import logging

import utils.logging as lg
from utils import general
from handler.settings import LOADED_TOKENS, load_tokens
from handler import library

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=["!", "?"], case_insensitive=True, intents=intents)


@bot.event
async def on_ready() -> None:
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.command(name="home")
async def home_page(ctx: commands.Context, target_url: str = "") -> None:
    if ctx.prefix == "?":
        await library.get_home_title(ctx)
        return
    await library.target_note_home(ctx, target_url)


if __name__ == "__main__":
    load_tokens()
    bot.run(LOADED_TOKENS.get("COMPEND_DISCORD_TOKEN"))
