import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Test Website", props={"href": "https://www.test.com"})
        node2 = HTMLNode("a", "Test Website", props={"href": "https://www.test.com"})
        self.assertEqual(node, node2)

    def test_values(self):
        node = HTMLNode("a", "Test Website", props={"href": "https://www.test.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Test Website")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.test.com"})

    def test_props_to_html_one(self):
        node = HTMLNode(props={"href": "https://www.test.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.test.com"')

    def test_props_to_html_two(self):
        node2 = HTMLNode(props={"href": "https://www.test.com", "target": "_blank"})
        self.assertEqual(
            node2.props_to_html(), ' href="https://www.test.com" target="_blank"'
        )

    def test_empty_is_none(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "Test Website", {"href": "https://www.test.com"})
        node2 = LeafNode("a", "Test Website", {"href": "https://www.test.com"})
        self.assertEqual(node, node2)

    def test_values(self):
        node = LeafNode("b", "Bold Text", {"href": "https://www.test.com"})
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "Bold Text")
        self.assertEqual(node.props, {"href": "https://www.test.com"})

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node, node2)

    def test_none_tag_error(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        self.assertRaises(ValueError, node.to_html)

    def test_none_children_error(self):
        node = ParentNode("b", None)
        self.assertRaises(ValueError, node.to_html)

    def test_empty_children(self):
        node = ParentNode("b", [])
        self.assertRaises(ValueError, node.to_html)

    def test_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
            {"test": "value"},
        )
        self.assertEqual(
            node.to_html(),
            '<p test="value"><b>Bold text</b></p>',
        )

    def test_nested_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "span",
                    [
                        LeafNode("b", "Bold text"),
                    ],
                ),
            ],
            {"test": "value"},
        )
        self.assertEqual(
            node.to_html(),
            '<p test="value"><span><b>Bold text</b></span></p>',
        )


if __name__ == "__main__":
    unittest.main()
