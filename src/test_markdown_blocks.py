import unittest
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    Blocktype,
    convert_code,
    convert_heading,
    convert_list,
    markdown_to_html_node,
)


class TestMarkdownBlocks(unittest.TestCase):
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

    def test_convert_code(self):
        with self.subTest("simple code block"):
            result = convert_code("```\nprint('hello')\n```")
            self.assertEqual(result.tag, "pre")
            self.assertEqual(result.children[0].tag, "code")
        with self.subTest("code block with language"):
            result = convert_code("```python\nprint('hello')\n```")
            self.assertEqual(result.tag, "pre")
            self.assertEqual(result.children[0].tag, "code")

    def test_convert_heading(self):
        with self.subTest("h1"):
            result = convert_heading("# Heading 1")
            self.assertEqual(result.tag, "h1")
        with self.subTest("h2"):
            result = convert_heading("## Heading 2")
            self.assertEqual(result.tag, "h2")
        with self.subTest("h3"):
            result = convert_heading("### Heading 3")
            self.assertEqual(result.tag, "h3")
        with self.subTest("h4"):
            result = convert_heading("#### Heading 4")
            self.assertEqual(result.tag, "h4")
        with self.subTest("h5"):
            result = convert_heading("##### Heading 5")
            self.assertEqual(result.tag, "h5")
        with self.subTest("h6"):
            result = convert_heading("###### Heading 6")
            self.assertEqual(result.tag, "h6")

    def test_markdown_to_html_node(self):
        with self.subTest("paragraph"):
            md = "This is a paragraph"
            result = markdown_to_html_node(md)
            self.assertIsNotNone(result)
        with self.subTest("heading and paragraph"):
            md = "# Heading\n\nThis is a paragraph"
            result = markdown_to_html_node(md)
            self.assertIsNotNone(result)
        with self.subTest("multiple blocks"):
            md = "# Heading\n\nParagraph 1\n\nParagraph 2"
            result = markdown_to_html_node(md)
            self.assertIsNotNone(result)

    def test_convert_list(self):
        with self.subTest("unordered list"):
            block = "- item 1\n- item 2\n- item 3"
            result = convert_list(block, ordered=False)
            self.assertEqual(result.tag, "ul")
            self.assertEqual(len(result.children), 3)
            self.assertEqual(result.children[0].tag, "li")
        with self.subTest("ordered list"):
            block = "1. item 1\n2. item 2\n3. item 3"
            result = convert_list(block, ordered=True)
            self.assertEqual(result.tag, "ol")
            self.assertEqual(len(result.children), 3)
            self.assertEqual(result.children[0].tag, "li")

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
