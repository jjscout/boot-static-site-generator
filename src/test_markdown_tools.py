import unittest
from markdown_tools import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
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
    
    def test_extract_title(self):
        with self.subTest("happy flow"):
            h1 = extract_title("# Hello")
            self.assertEqual(h1, "Hello")
        with self.subTest("two titles"):
            h1 = extract_title("# Hello\n# hwat")
            self.assertEqual(h1, "Hello")
        with self.subTest("no title"):
            with self.assertRaises(ValueError):
                h1 = extract_title("## Hello")

    



if __name__ == "__main__":
    unittest.main()
