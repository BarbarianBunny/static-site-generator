import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_uneq_text(self):
        node = TextNode("This is a text node 1", TextType.BOLD)
        node2 = TextNode("This is a text node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_uneq_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_empty_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

class TestToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("Test", TextType.TEXT)
        node2 = LeafNode(None, "Test")
        self.assertEqual(node.to_html_node(), node2)

    def test_bold(self):
        node = TextNode("Test", TextType.BOLD)
        node2 = LeafNode("b", "Test")
        self.assertEqual(node.to_html_node(), node2)

    def test_code(self):
        node = TextNode("Test", TextType.CODE)
        node2 = LeafNode("code", "Test")
        self.assertEqual(node.to_html_node(), node2)

    def test_italic(self):
        node = TextNode("Test", TextType.ITALIC)
        node2 = LeafNode("i", "Test")
        self.assertEqual(node.to_html_node(), node2)

    def test_image(self):
        node = TextNode("Test", TextType.IMAGE, "www.image.com")
        node2 = LeafNode("img", "", {"src": "www.image.com", "alt": "Test"})
        self.assertEqual(node.to_html_node(), node2)

    def test_link(self):
        node = TextNode("Test", TextType.LINK, "www.link.com")
        node2 = LeafNode("a", "Test", {"href": "www.link.com"})
        self.assertEqual(node.to_html_node(), node2)



if __name__ == "__main__":
    unittest.main()