import unittest

from utils import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and "
            "[another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_ignores_incomplete_links_and_images(self):
        self.assertEqual(extract_markdown_images("![alt](image.png"), [])
        self.assertEqual(extract_markdown_links("[label](https://example.com"), [])


if __name__ == "__main__":
    unittest.main()
