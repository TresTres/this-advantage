# __main__
from typing import Coroutine
import discord
import redis
from discord.ext import commands
import logging
from functools import wraps


import utils.logging as lg
from handler.settings import COMPEND_DISCORD_TOKEN, REDIS_PASSPHRASE
from handler import library, state_management

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(case_insensitive=True, intents=intents)
pages = bot.create_group(
    name="page", description="Commands relating to managing Notion pages"
)

redis_client = redis.Redis(password=REDIS_PASSPHRASE, decode_responses=True)
manager = state_management.StateManager(client=redis_client)


def deferring_command(func: Coroutine):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if isinstance(args[0], discord.ApplicationContext):
            await args[0].interaction.response.defer()
        await func(*args, **kwargs)

    return wrapper


@bot.event
async def on_ready() -> None:
    logger.info(
        f"Logged in as {bot.user} (ID: {bot.user.id}) on {len(bot.guilds)} guild(s)"
    )


@bot.slash_command(name="ping", description="Sends the bot's latency.")
async def ping(
    ctx: discord.ApplicationContext,
):  # a slash command will be created with the name "ping"
    logger.info(f"Received ping from {ctx.author}")
    await ctx.respond(f"Pong! Latency is {bot.latency}")


@pages.command(
    name="home",
    description="Set the home page with a url.  Invoking without an argument will ask for the current home page title",
)
@deferring_command
async def home_page(ctx: discord.ApplicationContext, target_url: str = "") -> None:
    if not target_url:
        await library.get_home_title(ctx, manager)
        return
    await library.target_note_home(ctx, manager, target_url)


@pages.command(
    name="session",
    description="Pick a session note page.  Requires the home page to be set.",
)
async def session_page(ctx: discord.ApplicationContext) -> None:
    await library.target_session_page(ctx, manager)


@bot.slash_command(
    name="current_session",
    description="Get info from current session.  Defaults to session number and title.",
    options=[
        discord.Option(
            name="full",
            type=str,
            default=False,
            description="Include full summary",
            choices=[
                discord.OptionChoice(name="Yes", value="1"),
                discord.OptionChoice(name="No", value=""),
            ],
        )
    ],
)
async def current_session(ctx: discord.ApplicationContext, full_info: str) -> None:
    await library.get_session_info(ctx, manager, bool(full_info))


if __name__ == "__main__":
    bot.run(COMPEND_DISCORD_TOKEN)
