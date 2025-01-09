import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="Test Website", props={"href":"https://www.test.com"})
        node2 = HTMLNode(tag="a", value="Test Website", props={"href":"https://www.test.com"})
        self.assertEqual(node, node2)

    def test_props_to_html_one(self):
        node = HTMLNode(props={"href":"https://www.test.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.test.com"')
    
    def test_props_to_html_two(self):
        node2 = HTMLNode(props={"href":"https://www.test.com", "target":"_blank"})
        self.assertEqual(node2.props_to_html(), ' href="https://www.test.com" target="_blank"')

    def test_empty_is_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

if __name__ == "__main__":
    unittest.main()