import unittest
from textnode import TextNode, TextType
from text_to_textnode import split_nodes_delimiter


class TestTextToTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        with self.subTest("no delimiter"):
            n = TextNode("text", text_type=TextType.TEXT)
            r = split_nodes_delimiter([n], "*", TextType.BOLD)
            self.assertEqual(
                r[0].text,
                "text",
            )

        with self.subTest("unclosed delimiter"):
            n = TextNode("*text", text_type=TextType.TEXT)
            with self.assertRaises(Exception):
                r = split_nodes_delimiter([n], "*", TextType.BOLD)
        with self.subTest("one bold"):
            n = TextNode("*text*", text_type=TextType.TEXT)
            r = split_nodes_delimiter([n], "*", TextType.BOLD)
            self.assertEqual(
                r[0],
                TextNode("text", TextType.BOLD),
            )

        with self.subTest("two bold"):
            n = TextNode("*text1* *text2*", text_type=TextType.TEXT)
            r = split_nodes_delimiter([n], "*", TextType.BOLD)
            self.assertEqual(
                r[0],
                TextNode("text1", TextType.BOLD),
            )
            self.assertEqual(
                r[1],
                TextNode(" ", TextType.TEXT),
            )
            self.assertEqual(
                r[2],
                TextNode("text2", TextType.BOLD),
            )

        with self.subTest("mix"):
            n = TextNode("*text1* `text2`", text_type=TextType.TEXT)
            r = split_nodes_delimiter([n], "*", TextType.BOLD)
            self.assertEqual(
                r[0],
                TextNode("text1", TextType.BOLD),
            )
            self.assertEqual(
                r[1],
                TextNode(" `text2`", TextType.TEXT),
            )
        with self.subTest("mix and undelimited"):
            n = TextNode(
                "text1 *text2* `text3` text4 *text5* text6",
                text_type=TextType.TEXT,
            )
            r = split_nodes_delimiter([n], "*", TextType.BOLD)
            self.assertEqual(
                r[0],
                TextNode("text1 ", TextType.TEXT),
            )
            self.assertEqual(
                r[1],
                TextNode("text2", TextType.BOLD),
            )
            self.assertEqual(
                r[2],
                TextNode(" `text3` text4 ", TextType.TEXT),
            )
            self.assertEqual(
                r[3],
                TextNode("text5", TextType.BOLD),
            )
            self.assertEqual(
                r[4],
                TextNode(" text6", TextType.TEXT),
            )
