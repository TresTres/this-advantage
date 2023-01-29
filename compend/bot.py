# __main__
import discord
from discord.ext import commands
import logging

import utils.logging as lg
from handler.settings import COMPEND_DISCORD_TOKEN
from handler import library, state_management

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(case_insensitive=True, intents=intents)
manager = state_management.StateManager()


@bot.event
async def on_ready() -> None:
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(
    ctx: discord.ApplicationContext,
):  # a slash command will be created with the name "ping"
    logger.info(f"Received ping from {ctx.author}")
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@bot.slash_command(
    name="home",
    description="Set the home page with a url.  Invoking without an argument will ask for the current home page title",
)
async def home_page(ctx: discord.ApplicationContext, target_url: str = "") -> None:
    if not target_url:
        await library.get_home_title(ctx, manager)
        return
    await library.target_note_home(ctx, manager, target_url)


@bot.slash_command(
    name="session",
    description="Pick a session note page.  Requires the home page to be set.",
)
async def session_page(ctx: discord.ApplicationContext) -> None:
    await library.target_session_page(ctx, manager)


@bot.slash_command(
    name="current_session",
    description="Get info from current session.  /current_session help to list available options",
)
async def current_session(ctx: discord.ApplicationContext, property: str) -> None:
    await library.get_session_title(ctx, manager)


if __name__ == "__main__":
    bot.run(COMPEND_DISCORD_TOKEN)
