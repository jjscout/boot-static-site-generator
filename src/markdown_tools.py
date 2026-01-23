import re
from typing import List, Tuple


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_title(text: str) -> str:
    h1 = re.findall(r"^# .*", text)
    if not h1:
        raise ValueError("No h1 title in text")
    h1 = h1[0][2:].strip()
    return h1
    