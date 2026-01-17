import unittest
from markdown_tools import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    block_to_block_type,
    Blocktype,
)


class TestMarkdownTools(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        matches = extract_markdown_images(
            "This is text with an [link](https://i.imgur.com)"
        )
        self.assertListEqual(matches, [])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com")], matches)
        matches = extract_markdown_links(
            "This is text with an ![img](https://i.imgur.com/lie.png)"
        )
        self.assertListEqual([], matches)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        with self.subTest("heading 1"):
            self.assertEqual(block_to_block_type("# heading1"), Blocktype.HEADING)
        with self.subTest("heading 2"):
            self.assertEqual(block_to_block_type("## heading1"), Blocktype.HEADING)
        with self.subTest("heading 3"):
            self.assertEqual(block_to_block_type("### heading1"), Blocktype.HEADING)
        with self.subTest("heading 4"):
            self.assertEqual(block_to_block_type("#### heading1"), Blocktype.HEADING)
        with self.subTest("heading 5"):
            self.assertEqual(block_to_block_type("##### heading1"), Blocktype.HEADING)
        with self.subTest("heading 6"):
            self.assertEqual(block_to_block_type("###### heading1"), Blocktype.HEADING)
        with self.subTest("heading 7 invalid"):
            self.assertNotEqual(
                block_to_block_type("######## heading1"), Blocktype.HEADING
            )

        with self.subTest("code"):
            self.assertEqual(
                block_to_block_type("```\n\n```"),
                Blocktype.CODE,
            )
        with self.subTest("not valid code"):
            self.assertNotEqual(
                block_to_block_type("``````"),
                Blocktype.CODE,
            )
            self.assertNotEqual(
                block_to_block_type("```\n``"),
                Blocktype.CODE,
            )
        with self.subTest("quote"):
            self.assertEqual(
                block_to_block_type("> quote\n> quote"),
                Blocktype.QUOTE,
            )
        with self.subTest("not quote"):
            self.assertEqual(
                block_to_block_type("> quote\n- quote"), Blocktype.PARAGRAPH
            )
        with self.subTest("unordered list item"):
            self.assertEqual(
                block_to_block_type("- quote\n- quote3"),
                Blocktype.UNORDERED_LIST,
            )
        with self.subTest("not unordered list"):
            self.assertEqual(
                block_to_block_type("- quote\n-quote3"),
                Blocktype.PARAGRAPH,
            )
            self.assertEqual(
                block_to_block_type("- quote\n. quote"), Blocktype.PARAGRAPH
            )
        with self.subTest("ordered list item"):
            self.assertEqual(
                block_to_block_type("1. quote\n2. q\n3. qq"), Blocktype.ORDERED_LIST
            )
        with self.subTest("not ordered list out of order"):
            self.assertEqual(
                block_to_block_type("1. quote\n2. q\n4. qq"), Blocktype.PARAGRAPH
            )
        with self.subTest("not ordered list item"):
            self.assertEqual(
                block_to_block_type("1. quote\n2. q\n> qq"), Blocktype.PARAGRAPH
            )
        with self.subTest("paragraph"):
            self.assertEqual(block_to_block_type("quote"), Blocktype.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
