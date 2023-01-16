# handler.library

import logging
import discord
import notion.api as notion
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


NOTE_HOME_PAGE: str = ""
NOTE_SESSION_PAGE: str = ""

async def target_note_home() -> str:
    """
    Defines the NOTE_HOME_PAGE global if not yet defined.
    TODO: This is something that should be stored in external memory.
    """
    if not NOTE_HOME_PAGE:
        NOTE_HOME_PAGE = await notion.find_page("Session Notes") 
    return NOTE_HOME_PAGE


async def specify_note_page(message: discord.Message, session_number: int) -> None: 
    """
    Defines the NOTE_SESSION_PAGE global by finding the session page to attach to
    TODO: This is something that should be stored in external memory.
    """
    # if not NOTE_SESSION_PAGE:
        

async def handle_quote(message: discord.Message) -> None:
    """
    Validate message, add a 🪶 reaction, and then confirm the message
    """
    
    await message.add_reaction("🪶")
