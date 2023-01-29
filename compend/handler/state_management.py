from collections import defaultdict
import redis
import logging
from typing import Any, Dict, Optional

import utils.logging as lg
from notion.data_types.data_classes import PageObject
from notion.api import get_page_object_for_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)


class UnsavedObjectException(Exception):
    """Attempted retrieval of unsaved object."""

    pass


class StateManager:
    """
    Two-level state management system for objects that persist for a bot.
    The redis client stores id information between bot lifecycles that can be used to retrieve notion page objects.
    Once the page objects are retrieved, they can be kept in session storage for immediate retrieval.
    """

    states: Dict[str, Any]
    client: redis.Redis

    def __init__(self, client: redis.Redis):
        logger.info("Initializing state manager")
        self.states = defaultdict(dict)
        self.client = client

    def save_page(self, guild_id: str, page_name: str, page_object: PageObject) -> None:
        """
        Save a page object to a guild's state.
        """
        guild_state = self.states[guild_id]
        guild_state.update({page_name: page_object})
        self.client.set(f"{guild_id}:{page_name}", page_object.id)
        logger.info("Saved page {guild_id}:{page_name}")

    def get_from_state(self, guild_id: str, page_name: str) -> PageObject:
        """
        Retrieve a page object from guild state.
        """
        if not (guild_state := self.states[guild_id]):
            raise UnsavedObjectException(
                f"{guild_id}:{page_name} has not been saved in local memory"
            )
        if not (page := guild_state.get(page_name, None)):
            raise UnsavedObjectException(
                f"{guild_id}:{page_name} has not been saved in local memory"
            )
        logger.info(f"Found page {guild_id}:{page_name}")
        return page

    async def get_page(self, guild_id: str, page_name: str) -> Optional[PageObject]:
        """
        Retrieve a page object from guild state or from client.
        """
        try:
            return self.get_from_state(guild_id, page_name)
        except UnsavedObjectException as uoe:
            logger.warn(uoe)
            if not (saved_id := self.client.get(f"{guild_id}:{page_name}")):
                logger.warn(f"{guild_id}:{page_name} has not been saved at all")
                return None
            page_obj = await get_page_object_for_id(saved_id)
            self.save_page(guild_id, page_name, page_obj)
            return page_obj
