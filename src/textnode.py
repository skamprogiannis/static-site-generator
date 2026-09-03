from enum import Enum
from urllib.parse import urlsplit

from leafnode import LeafNode
from utils import extract_markdown_images, extract_markdown_links


class TextType(Enum):
    NORMAL_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def _validated_url(text_node):
    if text_node.url is None:
        raise ValueError(f"a {text_node.text_type.value} node must have a URL")
    if text_node.url != text_node.url.strip() or any(
        character.isspace() for character in text_node.url
    ):
        raise ValueError("Markdown URLs cannot contain whitespace")

    scheme = urlsplit(text_node.url).scheme.lower()
    allowed_schemes = {"http", "https"}
    if text_node.text_type == TextType.LINK_TEXT:
        allowed_schemes.add("mailto")
    if scheme and scheme not in allowed_schemes:
        raise ValueError(f"unsupported URL scheme: {scheme}")
    return text_node.url


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode("a", text_node.text, {"href": _validated_url(text_node)})
        case TextType.IMAGE_TEXT:
            return LeafNode(
                "img",
                "",
                {"src": _validated_url(text_node), "alt": text_node.text},
            )
        case _:
            raise ValueError("text_node does not have a valid type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "":
        raise ValueError("delimiter cannot be empty")

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        
        delimiter_count = old_node.text.count(delimiter)
        if delimiter_count % 2 != 0:
            raise ValueError("invalid Markdown syntax: missing closing delimiter")

        split_text = old_node.text.split(delimiter)
        for i, text_chunk in enumerate(split_text):
            if text_chunk == "":
                continue
            
            if i % 2 == 1:
                new_node = TextNode(text_chunk, text_type)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(text_chunk, TextType.NORMAL_TEXT)
                new_nodes.append(new_node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        text_url_pairs = extract_markdown_images(old_node.text)
        if len(text_url_pairs) == 0:
            new_nodes.append(old_node)
            continue

        for pair in text_url_pairs:
            alt_text, url = pair[0], pair[1]

            sections = original_text.split(f"![{alt_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))

            original_text = sections[1]
            new_nodes.append(TextNode(alt_text, TextType.IMAGE_TEXT, url))
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        text_url_pairs = extract_markdown_links(old_node.text)
        if len(text_url_pairs) == 0:
            new_nodes.append(old_node)
            continue

        for pair in text_url_pairs:
            link_text, url = pair[0], pair[1]

            sections = original_text.split(f"[{link_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))

            original_text = sections[1]
            new_nodes.append(TextNode(link_text, TextType.LINK_TEXT, url))

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
