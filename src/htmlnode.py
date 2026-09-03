from html import escape
import re


ATTRIBUTE_NAME = re.compile(r"^[A-Za-z_:][A-Za-z0-9:._-]*$")


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        rendered_props = []
        for key, value in self.props.items():
            if not ATTRIBUTE_NAME.fullmatch(key):
                raise ValueError(f"invalid HTML attribute name: {key!r}")
            rendered_props.append(f' {key}="{escape(str(value), quote=True)}"')
        return "".join(rendered_props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
