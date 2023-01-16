# handler.function

import discord
from handler.library import handle_quote

LIBARY = {
    'quote': handle_quote,
    'get_summary': None,
    'set_session': None,
    'set_home_page': None, 
}

async def handle_command(command: str, message: discord.Message) -> None:
    """
    Select a function to run from the library using the command 
    """
    key = command.strip(' !')
    if key in LIBARY:
        await LIBARY[key](message)
    