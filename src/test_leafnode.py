import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        with self.subTest("no value"):
            node = LeafNode(tag=None, value=None)
            with self.assertRaises(ValueError):
                node.to_html()
        with self.subTest("no tag"):
            node = LeafNode(tag=None, value="content")
            self.assertEqual(node.to_html(), "content")
        with self.subTest("no props"):
            node = LeafNode(tag="p", value="content")
            self.assertEqual(node.to_html(), "<p>content</p>")
        with self.subTest("props"):
            node = LeafNode(
                tag="a",
                value="content",
                props={"href": "bla.com"},
            )
            self.assertEqual(node.to_html(), '<a href="bla.com">content</a>')

    def test_repr(self):
        node = LeafNode(
            tag="a",
            value="content",
            props={"href": "bla.com"},
        ) 
        self.assertEqual(
            str(node),
            "LeafNode(a, content, {'href': 'bla.com'})"
        )
