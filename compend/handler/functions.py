# handler.functions

import logging
import discord
import utils.logging as lg

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


async def handle_quote(message: discord.Message) -> None:
    logger.info(f"{message.content}")
