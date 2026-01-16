import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        with self.subTest("no tag"):
            node = ParentNode(tag=None, children=None)
            with self.assertRaises(ValueError):
                node.to_html()
        with self.subTest("no children"):
            node = ParentNode(tag="p", children=None)
            with self.assertRaises(ValueError):
                node.to_html()
        with self.subTest("no inner tag one child"):
            node = ParentNode(tag="p", children=[LeafNode(None, "content")])
            self.assertEqual(node.to_html(), "<p>content</p>")
        with self.subTest("no inner tag multiple child"):
            node = ParentNode(
                tag="p",
                children=[LeafNode(None, f"content{i}") for i in range(1, 4)],
            )
            self.assertEqual(
                node.to_html(),
                "<p>content1 content2 content3</p>",
            )
        with self.subTest("simple nested parent"):
            node = ParentNode(
                tag="p",
                children=[
                    ParentNode(
                        tag="p",
                        children=[LeafNode(None, "content")],
                    )
                ],
            )
            self.assertEqual(
                node.to_html(),
                "<p><p>content</p></p>",
            )
