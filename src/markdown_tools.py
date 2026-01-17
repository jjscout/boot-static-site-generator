import re
from typing import List, Tuple


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) ->  List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown: str) -> List[str]:
    return [b.strip() for b in markdown.split("\n\n") if b != ""]