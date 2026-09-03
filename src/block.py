from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    old_blocks = markdown.split("\n\n")
    filtered_blocks = []

    for block in old_blocks:
        trimmed_block = block.strip()
        if trimmed_block != "":
            filtered_blocks.append(trimmed_block)

    return filtered_blocks


def block_to_block_type(markdown_block):
    if re.match(r"^#{1,6}\s", markdown_block):
        return BlockType.HEADING

    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE

    lines = markdown_block.split("\n")

    is_quote = True
    is_unordered_list = True
    is_ordered_list = True
    for i, line in enumerate(lines):
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("- "):
            is_unordered_list = False
        if not line.startswith(f"{i+1}. "):
            is_ordered_list = False

    if is_quote:
        return BlockType.QUOTE
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
