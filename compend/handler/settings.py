import os
import logging
import utils.logging as lg


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


COMPEND_DISCORD_TOKEN = os.getenv("COMPEND_DISCORD_TOKEN", None)
COMPEND_NOTION_TOKEN = os.getenv("COMPEND_NOTION_TOKEN", None)
ACTIVE_NOTION_VERSION = "2022-06-28"
