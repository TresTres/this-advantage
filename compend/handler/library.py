# handler.library

from enum import Enum
import logging
from typing import Dict
from discord.ext import commands

from utils.general import split_first_token
import notion.api as notion
import notion.data as notion_data
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


NOTE_HOME_PAGE: Dict[str, str] = {}
NOTE_SESSION_PAGE: str = ""


MessageType = Enum("MessageType", ["FAIL", "SUCCESS", "INFO"])


async def emoji_reply(ctx: commands.Context, reply: str, msg_type: MessageType) -> None:
    """
    Reply to a message with an emoji and the attached reply content
    """
    emoji_lib = {
        MessageType.FAIL: "❌",
        MessageType.SUCCESS: "✅",
        MessageType.INFO: "ℹ️",
    }
    emoji = emoji_lib[msg_type]
    logger.info(f"{emoji} replying with: {reply}")
    await ctx.message.add_reaction(emoji)
    await ctx.message.reply(reply)


async def get_home_title(ctx: commands.Context) -> None:
    """
    Attempts to retrieve the title of the NOTE_HOME_PAGE
    TODO: This is something that should be stored in external memory
    """
    if not NOTE_HOME_PAGE:
        await emoji_reply(
            ctx, "Home page is not currently specified.", MessageType.INFO
        )
        return
    await emoji_reply(
        ctx,
        f"Home page currently set to {next(iter(NOTE_HOME_PAGE))}.",
        MessageType.INFO,
    )
    return


async def target_note_home(ctx: commands.Context, target_url: str) -> None:
    """
    Defines the NOTE_HOME_PAGE global using the sent url if not yet defined
    TODO: This is something that should be stored in external memory, not global vars
    """
    global NOTE_HOME_PAGE
    if not target_url:
        await get_home_title(ctx)
        return
    try:
        page_object = await notion.get_page_object_for_url(target_url)
        page_title = notion_data.get_title(page_object)
        NOTE_HOME_PAGE[page_title] = page_object["id"]
        await ctx.message.add_reaction("🏠")
        await emoji_reply(ctx, f"Home page set to {page_title}.", MessageType.SUCCESS)
    except ValueError as ve:
        await emoji_reply(ctx, str(ve), MessageType.FAIL)


"""
    try: 
        
        page_objects = await notion.find_page(args)
        


        await message.add_reaction("🏠")
        await emoji_reply(
            message, f"Home page set to {page_title}.", MessageType.SUCCESS
        )
    except ValueError as ve:
        await emoji_reply(message, str(ve), MessageType.FAIL)
"""
