from htmlnode import HTMLNode
from typing import Dict, List, Optional


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List["HTMLNode"],
        value: Optional[str] = None,
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            tag=tag,
            value=value,
            children=children,
            props=props,
        )

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node must have a tag")
        if not self.children:
            raise ValueError("parent node must have children")
        return (
            f"<{self.tag}{self.props_to_html() if self.props else ''}>"
            f"{' '.join(child.to_html() for child in self.children)}"
            f"</{self.tag}>"
        )

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
