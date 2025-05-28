import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is also text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_TextTypes(self):
        node1 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node3 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node4 = TextNode("This is a text node", TextType.CODE_TEXT)
        node5 = TextNode("This is a text node", TextType.LINK_TEXT)
        node6 = TextNode("This is a text node", TextType.IMAGE_TEXT) 
        nodes = [node1, node2, node3, node4, node5, node6]
        
        for i in range(len(nodes)):
            first_node = nodes[i]
            for j in range(i + 1, len(nodes)):
                second_node = nodes[j]
                self.assertNotEqual(first_node, second_node)
    
    def test_url(self):
        url_image_node = TextNode("This is an image text node", TextType.IMAGE_TEXT, url = "https://avatars.githubusercontent.com/u/48423146?s=96&v=4")
        image_node = TextNode("This is an image text node", TextType.IMAGE_TEXT)
        url_link_node = TextNode("This is a link text node", TextType.LINK_TEXT, url = "https://github.com/skamprogiannis")
        link_node = TextNode("This is a link text node", TextType.LINK_TEXT)

        self.assertNotEqual(url_image_node, image_node)
        self.assertNotEqual(url_link_node, link_node)

    def test_normal_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_text(self):
        pass

    def test_italic_text(self):
        pass

    def test_code_text(self):
        pass

    def test_link_text(self):
        pass

    def test_image_text(self):
        node = TextNode("This is an image node", TextType.IMAGE_TEXT, "https://avatars.githubusercontent.com/u/48423146?s=96&v=4")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://avatars.githubusercontent.com/u/48423146?s=96&v=4")
        self.assertEqual(html_node.props["alt"], node.text)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TEXT)

        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)

        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TEXT)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded", TextType.BOLD_TEXT),
                TextNode(" word and ", TextType.NORMAL_TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("bolded word", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("another", TextType.BOLD_TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word", TextType.NORMAL_TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD_TEXT),
                TextNode(" and ", TextType.NORMAL_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()