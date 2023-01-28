from strenum import StrEnum
from typing import Any, Dict, List
import json
import logging
import urllib3


from notion.data_types import PageObject, BlockObject, ChildrenResponseObject, BlockType
import utils.logging as lg
from handler.settings import COMPEND_NOTION_TOKEN, ACTIVE_NOTION_VERSION

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lg.attach_stdout_handler(logger)

HTTPRestMethod = StrEnum("RestMethod", ["GET", "POST"])

http_manager = urllib3.PoolManager(
    headers={
        "Authorization": f"Bearer {COMPEND_NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": ACTIVE_NOTION_VERSION,
    }
)

class FailedRequestException(Exception):
    """Failure of HTTP Request."""
    pass

class FailedURLParseException(Exception):
    """Failure to convert URL string to an ID"""
    pass

def create_url_target(endpoint: str) -> str:
    """
    Generates the url from the given endpoint
    """
    return f"https://api.notion.com/v1/{endpoint}"

def obtain_id_from_url(url: str) -> str:
    """
    Generates the id from a given url
    """
    parsed_url = urllib3.util.parse_url(url)
    path = parsed_url.path
    if ('notion' not in parsed_url.hostname) or (not path) or len(path) <= 32:
        raise FailedURLParseException(f"Invalid Notion page url: {url}")
    parsed_path = path[len(path) - 32 :]
    return f"{parsed_path[:8]}-{parsed_path[8:12]}-{parsed_path[12:16]}-{parsed_path[16:20]}-{parsed_path[20:32]}"

def unwrap_HTTP_response(response: urllib3.HTTPResponse) -> Dict[str, Any]:
    """
    If a response is valid, returns the content in dictionary format
    """
    if 300 > response.status >= 200:
        # reason OK
        return json.loads(response.data)
    logger.error(f"Request failed: {response.reason}")
    failure_body = json.loads(response.data)
    raise FailedRequestException(f"Failed: {failure_body['message']}")


async def request_notion_api(
    target: str, method: HTTPRestMethod, payload: Dict = None
) -> urllib3.HTTPResponse:
    """
    Get a response from the Notion API
    """
    if payload is None:
        payload = {}
    url = create_url_target(target)
    data = json.dumps(payload)
    return http_manager.request(method, url, body=data)

async def get_page_object_for_id(id: str) -> PageObject:
    """
    Attempts to get the page object for the given id
    """
    logger.info(f"Attemptng to retrieve page for id {id}")
    target = f"pages/{id}"
    response = await request_notion_api(target, HTTPRestMethod.GET)
    data = unwrap_HTTP_response(response)
    return PageObject(**data)


async def get_page_object_for_url(url: str) -> PageObject:
    """
    Attempts to get the page object for the given url
    """
    logger.info(f"Attempting to retrieve page for url {url}")
    parsed_id = obtain_id_from_url(url)
    return await get_page_object_for_id(parsed_id)

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
    resp = await request_notion_api("search", HTTPRestMethod.POST, payload)
    data = unwrap_HTTP_response(resp)
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


async def get_children(parent_id: str) -> ChildrenResponseObject:
    """
    Obtain the children objects of the given parent page
    """

    children_endpoint = f"blocks/{parent_id}/children"
    resp = await request_notion_api(children_endpoint, HTTPRestMethod.GET)
    return ChildrenResponseObject(**unwrap_HTTP_response(resp))


async def get_children_by_type(
    parent_id: str, block_type: BlockType
) -> List[BlockObject]:
    """
    Obtain the children objects from a page that match the given type
    """
    children = await get_children(parent_id)
    return [c for c in children.results if c.type == block_type]
