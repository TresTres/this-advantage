# handler.library

from enum import Enum
import logging
from typing import Dict
import discord

from utils.general import split_first_token
import notion.api as notion
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


NOTE_HOME_PAGE: Dict[str, str] = {}
NOTE_SESSION_PAGE: str = ""


MessageType = Enum("MessageType", ["FAIL", "SUCCESS", "INFO"])


async def emoji_reply(
    message: discord.Message, reply: str, msg_type: MessageType
) -> None:
    """
    Reply to a message with an emoji and the attached reply content
    """
    emoji_lib = {
        MessageType.FAIL: "❌",
        MessageType.SUCCESS: "✅",
        MessageType.INFO: "ℹ️",
    }
    await message.add_reaction(emoji_lib[msg_type])
    await message.reply(reply)


async def get_home_title(message: discord.Message) -> None:
    """
    Attempts to retrieve the title of the NOTE_HOME_PAGE
    """
    if not NOTE_HOME_PAGE:
        await emoji_reply(
            message, "Home page is not currently specified.", MessageType.INFO
        )
        return
    await emoji_reply(
        message, f"Home page set to {next(iter(NOTE_HOME_PAGE))}.", MessageType.INFO
    )
    return


async def target_note_home(message: discord.Message) -> None:
    """
    Defines the NOTE_HOME_PAGE global using the message content if not yet defined
    TODO: This is something that should be stored in external memory, not global vars
    """
    global NOTE_HOME_PAGE
    _, args = split_first_token(message.content)
    if not args:
        await get_home_title(message)
        return
    try:
        page_object = await notion.find_page(args)
        page_title = page_object["properties"]["title"]["title"][0]["plain_text"]
        NOTE_HOME_PAGE[page_title] = page_object["id"]
        await message.add_reaction("🏠")
        await emoji_reply(
            message, f"Home page set to {page_title}.", MessageType.SUCCESS
        )
    except ValueError as ve:
        await emoji_reply(message, str(ve), MessageType.FAIL)


async def specify_note_page(message: discord.Message, session_number: int) -> None:
    """
    Defines the NOTE_SESSION_PAGE global by finding the session page to attach to
    TODO: This is something that should be stored in external memory.
    """
    # if not NOTE_SESSION_PAGE:


async def add_quote(message: discord.Message) -> None:
    """
    Validate message, add a 🪶 reaction, and then confirm the message
    """
    await message.add_reaction("🪶")
