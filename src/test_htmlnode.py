import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props = {"href":"bla.com", "a":"b", "style":"bad"})
        self.assertEqual(
            ' href="bla.com" a="b" style="bad"',
            node.props_to_html(),
        )

    def test_to_html(self):
        node = HTMLNode(props = {"href":"bla.com", "a":"b", "style":"bad"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(
            "HTMLNode(None, None, None, None)",
            str(node),
        )


if __name__ == "__main__":
    unittest.main()
