# handler.functions

import logging
import discord
import notion.api as notion
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)




async def handle_quote(message: discord.Message, _ : str) -> None:
    """
    Validate message, add a 🪶 reaction, and then confirm the message
    """
    
    await message.add_reaction("🪶")
    await notion.create_page()
    