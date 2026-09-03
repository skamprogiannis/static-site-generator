from block import BlockType, block_to_block_type, markdown_to_blocks
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADING:
        level = len(block) - len(block.lstrip("#"))
        return ParentNode(f"h{level}", text_to_children(block[level:].strip()))

    if block_type == BlockType.CODE:
        lines = block.splitlines()
        language = lines[0][3:].strip()
        code = "\n".join(lines[1:-1])
        if code:
            code += "\n"
        props = {"class": f"language-{language}"} if language else None
        return ParentNode("pre", [LeafNode("code", code, props)])

    if block_type == BlockType.QUOTE:
        quote = "\n".join(
            line.removeprefix(">").lstrip() for line in block.splitlines()
        )
        return ParentNode("blockquote", text_to_children(quote))

    if block_type == BlockType.UNORDERED_LIST:
        items = [
            ParentNode("li", text_to_children(line[2:].strip()))
            for line in block.splitlines()
        ]
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        items = []
        for line in block.splitlines():
            _, text = line.split(". ", 1)
            items.append(ParentNode("li", text_to_children(text.strip())))
        return ParentNode("ol", items)

    paragraph = " ".join(line.strip() for line in block.splitlines())
    return ParentNode("p", text_to_children(paragraph))


def markdown_to_html_node(markdown):
    children = [block_to_html_node(block) for block in markdown_to_blocks(markdown)]
    return ParentNode("div", children, {"class": "markdown-body"})


def markdown_to_html(markdown):
    return markdown_to_html_node(markdown).to_html()
