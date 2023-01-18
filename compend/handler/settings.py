import os
import logging
import utils.logging as lg


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


EXPECTED_TOKENS = ["COMPEND_DISCORD_TOKEN", "COMPEND_NOTION_TOKEN"]
LOADED_TOKENS = {}
ACTIVE_NOTION_VERSION = "2022-06-28"


def load_tokens() -> None:
    """
    Load environment variables required for bot operation
    """
    logger.info("Loading environment variables...")
    for k in EXPECTED_TOKENS:
        LOADED_TOKENS.setdefault(k, os.getenv(k, ""))
        if not LOADED_TOKENS[k]:
            logger.error(f"Missing {k} environment variable.")
            exit(1)
