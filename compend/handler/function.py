# handler.function

from typing import Callable, Dict
import discord
from handler import library

SET_FUNCTIONS = {
    "help": None,
    "home": library.target_note_home,
    "quote": library.add_quote,
    "session": None,
}

GET_FUNCTIONS = {
    "help": None,
    "home": library.get_home_title,
    "quote": None,
}


async def execute_command_from_table(
    command_table: Dict[str, Callable], command: str, message: discord.Message
) -> None:
    """
    Attempt to run a command from the commmand table
    """
    if command in command_table:
        await command_table[command](message)
    else:
        await library.emoji_reply(
            message, f"Command {command} is not recognized.", library.MessageType.FAIL
        )


async def parse_command(command: str, message: discord.Message) -> None:
    """
    Select a function to run from the library using the command symbol:
    ! maps to setter functions
    ? maps to getter functions
    """
    set_symbol_pos = command.find("!")
    get_symbol_pos = command.find("?")

    if set_symbol_pos == get_symbol_pos:
        assert set_symbol_pos >= -1
        await library.emoji_reply(
            message,
            "Command format is invalid (must start with '?' or '!')",
            library.MessageType.FAIL,
        )
        return 

    if get_symbol_pos < set_symbol_pos:
        command_key = command.strip("?")
        await execute_command_from_table(GET_FUNCTIONS, command_key, message)
    else:
        command_key = command.strip("!")
        await execute_command_from_table(SET_FUNCTIONS, command_key, message)
