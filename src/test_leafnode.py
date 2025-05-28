import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        p_node = LeafNode("p", "Hello, world!")
        self.assertEqual(p_node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        a_node = LeafNode("a", "ValueError", {"href": "https://docs.python.org/3/library/exceptions.html#ValueError", "target": "_blank", 
                                            "rel": "noopener nofollow"})
        self.assertEqual(a_node.to_html(), "<a>ValueError</a>")

    def test_leaf_to_html_uneq(self):
        p_node = LeafNode("p", "Hello, world!")
        a_node = LeafNode("a", "ValueError", {"href": "https://docs.python.org/3/library/exceptions.html#ValueError", "target": "_blank", 
                                    "rel": "noopener nofollow"})
        self.assertNotEqual(p_node.to_html(), a_node.to_html())