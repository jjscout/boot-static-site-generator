from typing import Optional, Dict, List


class HTMLNode:
    def __init__(
        self,
        tag:Optional[str]=None,
        value:Optional[str]=None,
        children:Optional[List["HTMLNode"]]=None,
        props:Optional[Dict[str, str]]=None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return ''.join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
