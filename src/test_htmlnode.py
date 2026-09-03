import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
        def test_repr_eq(self):
            child_node1 = HTMLNode()
            child_node2 = HTMLNode()
            p_node = HTMLNode("p", "I am a paragraph", [child_node1, child_node2])
            self.assertEqual(repr(p_node), "HTMLNode(p, I am a paragraph, "
            "[HTMLNode(None, None, None, None), HTMLNode(None, None, None, None)], None)")

            self.assertEqual(repr(child_node1), repr(child_node2))

        def test_props_eq(self):
            span_node = HTMLNode("span", "the list of assert methods", None, {"class": "std std-ref"})
            a_node = HTMLNode("a", None, [span_node], {"class": "reference internal", "href": "#assert-methods", "target": "_self"})

            self.assertEqual(a_node.props_to_html(), ' class="reference internal" href="#assert-methods" target="_self"')
            self.assertEqual(span_node.props_to_html(), ' class="std std-ref"')

        def test_props_escape_attribute_values(self):
            node = HTMLNode("a", "example", props={"title": 'say "hello" & go'})

            self.assertEqual(
                node.props_to_html(), ' title="say &quot;hello&quot; &amp; go"'
            )

        def test_props_reject_invalid_attribute_names(self):
            node = HTMLNode("a", "example", props={'title onclick="alert(1)': "x"})

            with self.assertRaisesRegex(ValueError, "invalid HTML attribute name"):
                node.props_to_html()

        def test_props_uneq(self):
            span_node = HTMLNode("span", "the list of assert methods", None, {"class": "std std-ref"})
            a_node = HTMLNode("a", None, [span_node], {"class": "reference internal", "href": "#assert-methods", "target": "_self"})
            empty_node = HTMLNode()
            
            self.assertNotEqual(a_node.props_to_html(), span_node.props_to_html())
            self.assertNotEqual(a_node.props_to_html(), empty_node.props_to_html())
