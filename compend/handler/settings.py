import os
import logging
import utils.logging as lg


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

EXPECTED_TOKENS = ["COMPEND_DISCORD_TOKEN", "COMPEND_NOTION_TOKEN"]
LOADED_TOKENS = {token: os.getenv(token, "") for token in EXPECTED_TOKENS}
for k in EXPECTED_TOKENS:
    if not LOADED_TOKENS[k]:
        logger.error(f"Missing {k} environment variable.")
        exit(1)
            
ACTIVE_NOTION_VERSION = "2022-06-28"
