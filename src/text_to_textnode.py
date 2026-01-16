from textnode import TextNode, TextType
from typing import List
from markdown_tools import (
    extract_markdown_images,
    extract_markdown_links,
)


def split_nodes_delimiter(
    old_nodes: List[TextNode],
    delimiter: str,
    text_type: TextType,
) -> List[TextNode]:
    nn = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            nn.append(node)
            continue

        substrings = node.text.split(delimiter)
        if len(substrings) % 2 == 0:
            raise Exception(f"unclosed delimiter '{delimiter}' in node {node.text}")
        for i in range(len(substrings)):
            if substrings[i] == "":
                continue
            if i % 2 == 0:
                nn.append(TextNode(substrings[i], TextType.TEXT))
            else:
                nn.append(TextNode(substrings[i], text_type))
    return nn


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    nn = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            nn.append(node)
            continue

        original_text = node.text
        images_info = extract_markdown_images(node.text)
        if len(images_info) == 0:
            nn.append(node)
            continue
        for image in images_info:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown image")
            if sections[0] != "":
                nn.append(
                    TextNode(
                        text=sections[0],
                        text_type=TextType.TEXT,
                    )
                )
            nn.append(
                TextNode(
                    text=image[0],
                    text_type=TextType.IMAGE,
                    url = image[1]
                )
            )
            original_text = sections[1]
        if original_text != "":
            nn.append(
                TextNode(
                    text=original_text,
                    text_type=TextType.TEXT,
                )
            )
    return nn

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    nn = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            nn.append(node)
            continue

        original_text = node.text
        links_info = extract_markdown_links(node.text)
        if len(links_info) == 0:
            nn.append(node)
            continue
        for link in links_info:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown link")
            if sections[0] != "":
                nn.append(
                    TextNode(
                        text=sections[0],
                        text_type=TextType.TEXT,
                    )
                )
            nn.append(
                TextNode(
                    text=link[0],
                    text_type=TextType.LINK,
                    url = link[1]
                )
            )
            original_text = sections[1]
        if original_text:
            nn.append(
                TextNode(
                    text=original_text,
                    text_type=TextType.TEXT,
                )
            )

    return nn
