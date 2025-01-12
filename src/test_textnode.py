import unittest

from textnode import (
    TextNode,
    TextType,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
    markdown_to_text_blocks,
)
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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_non_text_is_unchanged(self):
        node = TextNode("Test *BOLD* in text", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), [node])

    def test_bold(self):
        node = TextNode("Test **BOLD** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**BOLD** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("BOLD", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("Test **BOLD**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
            ],
        )

    def test_code(self):
        node = TextNode("Test `CODE` text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("CODE", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("Test *ITALIC* text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TextType.ITALIC),
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("ITALIC", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_invalid_single_delimiter(self):
        node = TextNode("Test *ITALIC text", TextType.TEXT)
        self.assertRaises(
            ValueError, lambda: split_nodes_delimiter([node], "*", TextType.ITALIC)
        )

    def test_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_bold_in_italic_bold_first(self):
        node = TextNode("*italic **bold** italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertRaises(
            ValueError, lambda: split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        )

    def test_italic_in_bold_bold_first(self):
        node = TextNode("**bold *italic* bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold *italic* bold", TextType.BOLD),
            ],
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_find_0(self):
        tuple_list = extract_markdown_images(
            "This is a [Test Image](https://www.test.com/image)"
        )
        self.assertEqual(tuple_list, [])

    def test_find_1(self):
        tuple_list = extract_markdown_images(
            "This is a ![Test Image](https://www.test.com/image)"
        )
        self.assertEqual(tuple_list, [("Test Image", "https://www.test.com/image")])

    def test_find_2(self):
        tuple_list = extract_markdown_images(
            "This is a ![Test Image](https://www.test.com/image) and this is a ![Test Image 2](https://www.test.com/image2)"
        )
        self.assertEqual(
            tuple_list,
            [
                ("Test Image", "https://www.test.com/image"),
                ("Test Image 2", "https://www.test.com/image2"),
            ],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_link_only(self):
        tuple_list = extract_markdown_links("[Test Link](https://www.test.com/link)")
        self.assertEqual(tuple_list, [("Test Link", "https://www.test.com/link")])

    def test_find_1(self):
        tuple_list = extract_markdown_links(
            "This is a [Test Link](https://www.test.com/link)"
        )
        self.assertEqual(tuple_list, [("Test Link", "https://www.test.com/link")])

    def test_find_2(self):
        tuple_list = extract_markdown_links(
            "This is a [Test Link](https://www.test.com/link) and this is a [Test Link 2](https://www.test.com/link2)"
        )
        self.assertEqual(
            tuple_list,
            [
                ("Test Link", "https://www.test.com/link"),
                ("Test Link 2", "https://www.test.com/link2"),
            ],
        )


class TestSplitNodesImages(unittest.TestCase):
    def test_no_image(self):
        node = TextNode(
            "This is a False Test Image https://www.test.com/image between words.",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode(
                    "This is a False Test Image https://www.test.com/image between words.",
                    TextType.TEXT,
                ),
            ],
        )

    def test_text_sandwich(self):
        node = TextNode(
            "This is a ![Test Image](https://www.test.com/image) between words.",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Image", TextType.IMAGE, "https://www.test.com/image"),
                TextNode(" between words.", TextType.TEXT),
            ],
        )

    def test_image_1(self):
        node = TextNode(
            "This is a ![Test Image](https://www.test.com/image)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Image", TextType.IMAGE, "https://www.test.com/image"),
            ],
        )

    def test_image_2(self):
        node = TextNode(
            "This is a ![Test Image](https://www.test.com/image) and this is a ![Test Image 2](https://www.test.com/image2)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Image", TextType.IMAGE, "https://www.test.com/image"),
                TextNode(" and this is a ", TextType.TEXT),
                TextNode("Test Image 2", TextType.IMAGE, "https://www.test.com/image2"),
            ],
        )

    def test_no_nodes(self):
        self.assertEqual(split_nodes_links([]), [])

    def test_multiple_nodes(self):
        node = TextNode(
            "This is a ![Test Image](https://www.test.com/image)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_images([node, node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Image", TextType.IMAGE, "https://www.test.com/image"),
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Image", TextType.IMAGE, "https://www.test.com/image"),
            ],
        )


class TestSplitNodesLinks(unittest.TestCase):
    def test_no_link(self):
        node = TextNode(
            "This is a False Test Link https://www.test.com/link between words.",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode(
                    "This is a False Test Link https://www.test.com/link between words.",
                    TextType.TEXT,
                ),
            ],
        )

    def test_text_sandwich(self):
        node = TextNode(
            "This is a [Test Link](https://www.test.com/link) between words.",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Link", TextType.LINK, "https://www.test.com/link"),
                TextNode(" between words.", TextType.TEXT),
            ],
        )

    def test_link_1(self):
        node = TextNode(
            "This is a [Test Link](https://www.test.com/link)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Link", TextType.LINK, "https://www.test.com/link"),
            ],
        )

    def test_link_2(self):
        node = TextNode(
            "This is a [Test Link](https://www.test.com/link) and this is a [Test Link 2](https://www.test.com/link2)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_links([node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Link", TextType.LINK, "https://www.test.com/link"),
                TextNode(" and this is a ", TextType.TEXT),
                TextNode("Test Link 2", TextType.LINK, "https://www.test.com/link2"),
            ],
        )

    def test_no_nodes(self):
        self.assertEqual(split_nodes_links([]), [])

    def test_multiple_nodes(self):
        node = TextNode(
            "This is a [Test Link](https://www.test.com/link)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_links([node, node]),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Link", TextType.LINK, "https://www.test.com/link"),
                TextNode("This is a ", TextType.TEXT),
                TextNode("Test Link", TextType.LINK, "https://www.test.com/link"),
            ],
        )

    def test_text_is_link(self):
        node = TextNode("[Text](Link)", TextType.TEXT)
        self.assertEqual(
            split_nodes_links([node]), [TextNode("Text", TextType.LINK, "Link")]
        )


class TestTextToTextNode(unittest.TestCase):
    def test_text(self):
        nodes = text_to_textnodes("Test Text")
        self.assertEqual(nodes, [TextNode("Test Text", TextType.TEXT)])

    def test_images(self):
        nodes = text_to_textnodes("![Test](Image)")
        self.assertEqual(nodes, [TextNode("Test", TextType.IMAGE, "Image")])

    def test_links(self):
        nodes = text_to_textnodes("[Test](Link)")
        self.assertEqual(nodes, [TextNode("Test", TextType.LINK, "Link")])

    def test_code(self):
        nodes = text_to_textnodes("Test `Code`")
        self.assertEqual(
            nodes, [TextNode("Test ", TextType.TEXT), TextNode("Code", TextType.CODE)]
        )

    def test_bold(self):
        nodes = text_to_textnodes("Test **Bold**")
        self.assertEqual(
            nodes, [TextNode("Test ", TextType.TEXT), TextNode("Bold", TextType.BOLD)]
        )

    def test_italics(self):
        nodes = text_to_textnodes("Test *Italic*")
        self.assertEqual(
            nodes,
            [TextNode("Test ", TextType.TEXT), TextNode("Italic", TextType.ITALIC)],
        )

    def test_in_order(self):
        nodes = text_to_textnodes(
            "Test ![Test](Image) [Test](Link) `Code` **Bold** *Italic*"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("Test", TextType.IMAGE, "Image"),
                TextNode(" ", TextType.TEXT),
                TextNode("Test", TextType.LINK, "Link"),
                TextNode(" ", TextType.TEXT),
                TextNode("Code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("Italic", TextType.ITALIC),
            ],
        )

    def test_in_reverse_order(self):
        nodes = text_to_textnodes(
            "Test *Italic* **Bold** `Code` [Test](Link) ![Test](Image)"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Test ", TextType.TEXT),
                TextNode("Italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("Code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("Test", TextType.LINK, "Link"),
                TextNode(" ", TextType.TEXT),
                TextNode("Test", TextType.IMAGE, "Image"),
            ],
        )


class TestMarkdownToTextBlocks(unittest.TestCase):
    def test_no_text(self):
        blocks = markdown_to_text_blocks("")
        self.assertEqual(blocks, [])

    def test_1_block(self):
        blocks = markdown_to_text_blocks("Test")
        self.assertEqual(blocks, ["Test"])

    def test_removes_leading_whitespace(self):
        blocks = markdown_to_text_blocks(" Test")
        self.assertEqual(blocks, ["Test"])

    def test_removes_trailing_whitespace(self):
        blocks = markdown_to_text_blocks("Test ")
        self.assertEqual(blocks, ["Test"])

    def test_removes_whitespace(self):
        blocks = markdown_to_text_blocks(" Test ")
        self.assertEqual(blocks, ["Test"])

    def test_removes_leading_newline(self):
        blocks = markdown_to_text_blocks("\nTest")
        self.assertEqual(blocks, ["Test"])

    def test_removes_trailing_newline(self):
        blocks = markdown_to_text_blocks("Test\n")
        self.assertEqual(blocks, ["Test"])

    def test_removes_surrounding_newlines(self):
        blocks = markdown_to_text_blocks("\nTest\n")
        self.assertEqual(blocks, ["Test"])

    def test_2_blocks(self):
        blocks = markdown_to_text_blocks("Test\n\nTest2")
        self.assertEqual(blocks, ["Test", "Test2"])

    def test_2_blocks_multiline(self):
        blocks = markdown_to_text_blocks("Test\n\nTest2\nTest2")
        self.assertEqual(blocks, ["Test", "Test2\nTest2"])

    def test_2_blocks_multiline_whitespace(self):
        blocks = markdown_to_text_blocks(
            """Test
                                         
Test2
Test2 
"""
        )
        self.assertEqual(blocks, ["Test", "Test2\nTest2"])

    def test_block_dev_example(self):
        blocks = markdown_to_text_blocks(
            """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        )
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item""",
            ],
        )


if __name__ == "__main__":
    unittest.main()
