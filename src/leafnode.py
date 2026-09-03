from html import escape

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("a leaf node must have a value")

        escaped_value = escape(str(self.value))
        if self.tag is None:
            return escaped_value

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        if self.tag in self.VOID_TAGS:
            return opening_tag

        return f"{opening_tag}{escaped_value}</{self.tag}>"
