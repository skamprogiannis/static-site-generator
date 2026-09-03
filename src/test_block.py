import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block of text"])

    def test_markdown_to_blocks_empty_blocks(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is lowly paragraph block"), BlockType.PARAGRAPH
        )
        self.assertNotEqual(
            block_to_block_type("- This is not a paragraph block"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(
            block_to_block_type("# This is a heading block"), BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("##### This is also a heading block"), BlockType.HEADING
        )
        self.assertNotEqual(
            block_to_block_type("This is not a heading block"), BlockType.HEADING
        )
        self.assertNotEqual(
            block_to_block_type(
                "####### This is not a heading block either, 7 hashtags? Who does that?"
            ),
            BlockType.HEADING,
        )

    def test_block_to_block_type_code(self):
        self.assertEqual(
            block_to_block_type("```This is a code block```"), BlockType.CODE
        )
        self.assertNotEqual(
            block_to_block_type("``This is not a code block``"), BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        self.assertEqual(
            block_to_block_type("> This is a quote block"), BlockType.QUOTE
        )
        self.assertNotEqual(
            block_to_block_type("< This is not a quote block``"), BlockType.QUOTE
        )

    def test_block_to_block_type_unordered(self):
        self.assertEqual(
            block_to_block_type("- This is an unordered\n- list block"),
            BlockType.UNORDERED_LIST,
        )
        self.assertNotEqual(
            block_to_block_type("!This is not an unordered\n!-list block"),
            BlockType.UNORDERED_LIST,
        )
        self.assertNotEqual(
            block_to_block_type("-This is not an unordered\n-list block either"),
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_block_type_ordered(self):
        self.assertEqual(
            block_to_block_type("1. First point \n2. Second point\n3. Third point"),
            BlockType.ORDERED_LIST,
        )
        self.assertNotEqual(
            block_to_block_type("1. First point\n3. Third point"),
            BlockType.ORDERED_LIST,
        )
        self.assertNotEqual(
            block_to_block_type("1! First point\n2! Second point"),
            BlockType.ORDERED_LIST,
        )


if __name__ == "__main__":
    unittest.main()
