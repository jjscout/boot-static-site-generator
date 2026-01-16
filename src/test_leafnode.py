import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        with self.subTest("no value"):
            node = LeafNode()
            with self.assertRaises(ValueError):
                node.to_html()
        with self.subTest("no tag"):
            pass