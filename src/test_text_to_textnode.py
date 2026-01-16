import unittest

from text_to_textnode import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


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

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcjkz.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes[1],
            TextNode(
                text="image",
                text_type=TextType.IMAGE,
                url="https://i.imgur.com/zjjcjkz.png",
            ),
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes[1],
            TextNode(
                text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"
            ),
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes2(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
