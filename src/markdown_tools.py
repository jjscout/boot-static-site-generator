import re
from typing import List, Tuple
from enum import Enum


class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def markdown_to_blocks(markdown: str) -> List[str]:
    return [b.strip() for b in markdown.split("\n\n") if b != ""]


def block_to_block_type(block: str) -> Blocktype:
    lines = block.split("\n")
    if block.startswith(tuple("#" * (i + 1) + " " for i in range(6))):
        return Blocktype.HEADING
    if block.startswith("```\n") and block.endswith("```") and len(lines) > 1:
        return Blocktype.CODE
    if block.startswith("> "):
        if any(not line.startswith("> ") for line in lines):
            return Blocktype.PARAGRAPH
        return Blocktype.QUOTE
    if block.startswith("- "):
        if any(not line.startswith("- ") for line in lines):
            return Blocktype.PARAGRAPH
        return Blocktype.UNORDERED_LIST
    if block.startswith("1. "):
        if any(not line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
            return Blocktype.PARAGRAPH
        return Blocktype.ORDERED_LIST
    return Blocktype.PARAGRAPH
