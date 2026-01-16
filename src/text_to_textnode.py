from textnode import TextNode, TextType
from typing import List


def split_nodes_delimiter(
    old_nodes: List[TextNode],
    delimiter: str,
    text_type: TextType,
):
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
