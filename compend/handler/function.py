# handler.function

import discord
from handler.library import handle_quote

LIBRARY = {
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
    if key in LIBRARY:
        await LIBRARY[key](message)
    else:
        await message.add_reaction("❌")
        await message.reply(f"Command {command} is invalid.")
    