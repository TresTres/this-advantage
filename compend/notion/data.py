from typing import Dict


def get_title(page_obj: Dict) -> str:

    return "".join(page_obj["properties"]["title"]["title"][0]["plain_text"])
