from typing import List
from pydantic import BaseModel

from notion.data_types.data_classes import BlockObject, ChildPageObject


class ChildrenResponseObject(BaseModel):
    object: str = "list"
    results: List[BlockObject]
    has_more: bool
    type: str = "block"


__all__ = ["ChildrenResponseObject"]
