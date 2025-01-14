import unittest

from htmlnode import ParentNode, LeafNode
from block_handling import (
    BlockType,
    markdown_to_text_blocks,
    is_block_type_code,
    is_block_type_heading,
    is_block_type_ordered_list,
    is_block_type_quote,
    is_block_type_unordered_list,
    block_to_block_type,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
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

    def test_block_code(self):
        blocks = markdown_to_text_blocks(
            """Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Hello, World!")
}
```"""
        )
        self.assertEqual(
            blocks,
            [
                "Here's what `elflang` looks like (the perfect coding language):",
                """```
func main(){
    fmt.Println("Hello, World!")
}
```""",
            ],
        )

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


class TestParagraphToHTMLNode(unittest.TestCase):
    def test_text(self):
        text = "Test"
        html_node = paragraph_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<p>Test</p>")

    def test_bold(self):
        text = "**Test**"
        html_node = paragraph_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<p><b>Test</b></p>")


class TestHeadingToHTMLNode(unittest.TestCase):
    def test_text(self):
        text = "# Test"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h1>Test</h1>")

    def test_2(self):
        text = "## Test"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h2>Test</h2>")

    def test_3(self):
        text = "### Test"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h3>Test</h3>")

    def test_4(self):
        text = "#### Test"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h4>Test</h4>")

    def test_5(self):
        text = "##### Test"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h5>Test</h5>")

    def test_6(self):
        text = "###### Test"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h6>Test</h6>")

    def test_bold(self):
        text = "# **Test**"
        html_node = heading_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<h1><b>Test</b></h1>")


class TestCodeToHTMLNode(unittest.TestCase):
    def test_1(self):
        text = "```Test```"
        html_node = code_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<pre><code>Test</code></pre>")

    def test_2(self):
        text = "```Test\nTest```"
        html_node = code_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<pre><code>Test\nTest</code></pre>")


class TestQuoteToHTMLNode(unittest.TestCase):
    def test_1(self):
        text = "> Test"
        html_node = quote_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<blockquote>Test</blockquote>")

    def test_2(self):
        text = "> Test\n> Test"
        html_node = quote_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<blockquote>Test\nTest</blockquote>")

    def test_1_no_space(self):
        text = ">Test"
        html_node = quote_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<blockquote>Test</blockquote>")

    def test_2_no_space(self):
        text = ">Test\n> Test"
        html_node = quote_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<blockquote>Test\nTest</blockquote>")


class TestUnorderedListToHTMLNode(unittest.TestCase):
    def test_1_dash(self):
        text = "- Test"
        html_node = unordered_list_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<ul><li>Test</li></ul>")

    def test_1_star(self):
        text = "* Test"
        html_node = unordered_list_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<ul><li>Test</li></ul>")

    def test_2_dash(self):
        text = "- Test\n- Test"
        html_node = unordered_list_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<ul><li>Test</li><li>Test</li></ul>")


class TestOrderedListToHTMLNode(unittest.TestCase):
    def test_1_dash(self):
        text = "1. Test"
        html_node = ordered_list_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<ol><li>Test</li></ol>")

    def test_2_dash(self):
        text = "1. Test\n2. Test"
        html_node = ordered_list_to_html_node(text)
        html = html_node.to_html()
        self.assertEqual(html, "<ol><li>Test</li><li>Test</li></ol>")


class TestIsBlockTypeHeading(unittest.TestCase):
    def test_1_heading(self):
        text = "# Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, True)

    def test_2_heading(self):
        text = "## Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, True)

    def test_3_heading(self):
        text = "### Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, True)

    def test_4_heading(self):
        text = "#### Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, True)

    def test_5_heading(self):
        text = "##### Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, True)

    def test_6_heading(self):
        text = "###### Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, True)

    def test_multiline(self):
        text = "# Test\ntest"
        result = is_block_type_heading(text)
        self.assertEqual(result, False)

    def test_missing_space(self):
        text = "#Test"
        result = is_block_type_heading(text)
        self.assertEqual(result, False)


class TestIsBlockTypeCode(unittest.TestCase):
    def test_1_line(self):
        text = "```Test```"
        result = is_block_type_code(text)
        self.assertEqual(result, True)

    def test_2_line(self):
        text = "```Test\nTest```"
        result = is_block_type_code(text)
        self.assertEqual(result, True)

    def test_3_line(self):
        text = "```Test \n Test \n Test```"
        result = is_block_type_code(text)
        self.assertEqual(result, True)

    def test_1_ticks(self):
        text = "`Test`"
        result = is_block_type_code(text)
        self.assertEqual(result, False)

    def test_2_ticks(self):
        text = "``Test``"
        result = is_block_type_code(text)
        self.assertEqual(result, False)

    def test_multiline(self):
        text = """```
func main(){
    fmt.Println("Hello, World!")
}
```"""
        result = is_block_type_code(text)
        self.assertEqual(result, True)


class TestIsBlockTypeQuote(unittest.TestCase):
    def test_no_quote(self):
        text = "Text"
        result = is_block_type_quote(text)
        self.assertEqual(result, False)

    def test_no_space(self):
        text = ">Text"
        result = is_block_type_quote(text)
        self.assertEqual(result, True)

    def test_excess_space(self):
        text = ">    Text"
        result = is_block_type_quote(text)
        self.assertEqual(result, True)

    def test_1_line(self):
        text = "> Text"
        result = is_block_type_quote(text)
        self.assertEqual(result, True)

    def test_2_line(self):
        text = "> Text\n> Text"
        result = is_block_type_quote(text)
        self.assertEqual(result, True)

    def test_3_line(self):
        text = "> Text\n> Text\n> Text"
        result = is_block_type_quote(text)
        self.assertEqual(result, True)


class TestIsBlockTypeUnorderedList(unittest.TestCase):
    def test_no_space_star(self):
        text = "*Test"
        result = is_block_type_unordered_list(text)
        self.assertEqual(result, False)

    def test_no_space_dash(self):
        text = "-Test"
        result = is_block_type_unordered_list(text)
        self.assertEqual(result, False)

    def test_1_line_star(self):
        text = "* Test"
        result = is_block_type_unordered_list(text)
        self.assertEqual(result, True)

    def test_1_line_dash(self):
        text = "- Test"
        result = is_block_type_unordered_list(text)
        self.assertEqual(result, True)

    def test_2_line_star(self):
        text = "* Test\n* Test"
        result = is_block_type_unordered_list(text)
        self.assertEqual(result, True)

    def test_2_line_dash(self):
        text = "- Test\n- Test"
        result = is_block_type_unordered_list(text)
        self.assertEqual(result, True)


class TestIsBlockTypeOrderedList(unittest.TestCase):
    def test_1_line(self):
        text = "1. Test"
        result = is_block_type_ordered_list(text)
        self.assertEqual(result, True)

    def test_10_line(self):
        text = "1. Test\n2. Test\n3. Test\n4. Test\n5. Test\n6. Test\n7. Test\n8. Test\n9. Test\n10. Test"
        result = is_block_type_ordered_list(text)
        self.assertEqual(result, True)

    def test_no_space(self):
        text = "1.Test"
        result = is_block_type_ordered_list(text)
        self.assertEqual(result, False)

    def test_wrong_numbers(self):
        text = "1. Test\n.3 Test"
        result = is_block_type_ordered_list(text)
        self.assertEqual(result, False)

    def test_wrong_start_number(self):
        text = "2. Test\n.3 Test"
        result = is_block_type_ordered_list(text)
        self.assertEqual(result, False)


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = "Test"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading(self):
        text = "# Test"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
        text = "```Test\nTest```"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        text = "> Test\n> Test"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        text = "* Test"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        text = "1. Test\n2. Test"
        result = block_to_block_type(text)
        self.assertEqual(result, BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
