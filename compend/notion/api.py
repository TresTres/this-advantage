from typing import Dict
import requests, json

from handler.settings import LOADED_TOKENS, ACTIVE_NOTION_VERSION

NOTION_PAGE_ID = "2fca0c39-6af3-41d5-9d9d-e2455377e3c3"


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
        "Notion-Version": ACTIVE_NOTION_VERSION
    }

async def create_page() -> None:
    """
    Test method to create a new and empty notion page
    """
    
    url = create_url_target("pages")
    headers = construct_headers()
    payload = {
        "parent": { "page_id": NOTION_PAGE_ID },
        "properties": {
            "title": [
                {
                    "text": {
                        "content": "Test page"
                    }
                }
            ]
        }
    }

    data = json.dumps(payload)
    res = requests.request("POST", url, headers=headers, data=data)    
    