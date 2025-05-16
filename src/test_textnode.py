import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()