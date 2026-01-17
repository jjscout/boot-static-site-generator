import re
from enum import Enum
from typing import TYPE_CHECKING, List

from leafnode import LeafNode
from parentnode import ParentNode
from text_to_textnode import text_to_textnodes
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)

if TYPE_CHECKING:
    from htmlnode import HTMLNode


class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def convert_heading(heading: str) -> LeafNode:
    level = 0
    while heading[level] == "#":
        level += 1
    return LeafNode(tag=f"h{level}", value=heading[level + 1 :])


def convert_code(code: str) -> ParentNode:
    text = code[4:-3]
    node = text_node_to_html_node(TextNode(text=text, text_type=TextType.TEXT))
    node = ParentNode(tag="code", children=[node])
    node = ParentNode(tag="pre", children=[node])
    return node


def text_to_children(text: str) -> List["HTMLNode"]:
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]


def convert_list(block: str, ordered: bool) -> ParentNode:
    list_items_nodes = []
    for line in block.split("\n"):
        line = line.lstrip("- ") if not ordered else line.lstrip("0123456789. ")
        list_items_nodes.append(ParentNode(tag="li", children=text_to_children(line)))
    tag = "ol" if ordered else "ul"
    return ParentNode(tag=tag, children=list_items_nodes)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case Blocktype.HEADING:
                nodes.append(convert_heading(block))
            case Blocktype.CODE:
                node = convert_code(block)
                nodes.append(node)
            case Blocktype.QUOTE:
                block = " ".join(line.lstrip("> ") for line in block.split("\n"))
                nodes.append(
                    ParentNode(
                        tag="blockquote",
                        children=text_to_children(block),
                    )
                )
            case Blocktype.UNORDERED_LIST:
                nodes.append(convert_list(block, ordered=False))
            case Blocktype.ORDERED_LIST:
                nodes.append(convert_list(block, ordered=True))
            case Blocktype.PARAGRAPH:
                nodes.append(
                    ParentNode(
                        tag="p",
                        children=text_to_children(block),
                    )
                )
    return ParentNode(tag="div", children=nodes)
