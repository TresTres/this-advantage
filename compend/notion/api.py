from enum import Enum
from typing import Any, Dict, List
import requests, json
import logging

import utils.logging as lg
from handler.settings import LOADED_TOKENS, ACTIVE_NOTION_VERSION

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

RestMethod = Enum("RestMethod", ["GET", "POST"])


class FailedRequestException(Exception):
    """While not necessarily a fast-fail, should be treated as an exception"""

    pass


def create_url_target(endpoint: str) -> str:
    """
    Generates the url from the given endpoint
    """
    return f"https://api.notion.com/v1/{endpoint}"


def construct_headers() -> Dict[str, str]:
    """
    Construct API request headers
    """
    token = LOADED_TOKENS.get("COMPEND_NOTION_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": ACTIVE_NOTION_VERSION,
    }


def unwrap_response(response: requests.Response) -> Dict[str, Any]:
    """
    If a response is valid, returns the content in dictionary format
    """
    if response.ok:
        return json.loads(response.content)
    logger.error(f"Request failed: {response.reason}")
    content = json.loads(response.content)
    raise FailedRequestException(f"Failed: {content['message']}")


async def request_notion_api(
    target: str, method: RestMethod, payload: Dict = None
) -> requests.Response:
    """
    Get a response from the Notion API
    """
    if payload is None:
        payload = {}
    url = create_url_target(target)
    headers = construct_headers()
    data = json.dumps(payload)
    return requests.request(method.name, url, headers=headers, data=data)


async def find_page(title: str) -> List[Dict]:
    """
    Obtains the object of a specific Notion page
    """
    payload = {
        "query": title,
        "filter": {
            "property": "object",
            "value": "page",
        },
        "page_size": 5,
    }
    resp = await request_notion_api("search", RestMethod.POST, payload)
    data = unwrap_response(resp)
    if not data["results"]:
        ve_message = f"No result for page matching title `{title}`."
        logger.error(ve_message)
        raise ValueError(ve_message)

    logger.info(f"Found {len(data['results'])} results searching for page `{title}`")
    return data["results"]


async def find_child_page(parent_id: str, child_title: str) -> str:
    """
    Search by name for the child page of a given parent page
    """


async def get_children(parent_id: str) -> Dict[str, List]:
    """
    Obtain the children objects of the given parent page,
    separated by block type
    """
    children_endpoint = f"blocks/{parent_id}/children"
    resp = await request_notion_api(children_endpoint, RestMethod.GET)
    data = unwrap_response(resp)

    children = {}
    for obj in data["results"]:
        obj_type = obj["object"]
        children.setdefault(obj_type, [])
        children[obj_type].append(obj)

    return children
