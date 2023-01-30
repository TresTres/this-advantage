from typing import List
from pydantic import BaseModel
from notion.data_types.data_classes import BlockObject


class ChildrenResponseObject(BaseModel):
    object: str = "list"
    results: List[BlockObject]
    has_more: bool
    type: str = "block"
    
    
    def get_all_under_header(self, heading_name: str) -> List[BlockObject]:
        """
        Retrieves all block objects that are under a header in the page
        TODO: Depending on how many search and access methods we'll need, it'll be worth to heapify the result content.
        """
        headers = iter((idx, r) for (idx, r) in enumerate(self.results) if r.active_heading)
        for h in headers:
            if heading_name.lower() in h[1].active_heading.text_content.lower():
                start_index = h[0] + 1
                try:
                    # collect all the following elements
                    next_h = next(headers)
                    return self.results[start_index:next_h[0]]
                except StopIteration:
                    return self.results[start_index:]
        return []
    

__all__ = ["ChildrenResponseObject"]
