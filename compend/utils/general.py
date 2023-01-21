from typing import Tuple


def split_first_token(string: str, sep: str = " ") -> Tuple[str, str]:
    """
    Split the first word from the rest of a given string
    """
    if not string:
        return "", ""
    split_content = string.split(sep, 1)
    return split_content[0].strip(), "".join(split_content[1:])
