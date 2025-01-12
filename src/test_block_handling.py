import unittest

from block_handling import (
    markdown_to_text_blocks,
    is_block_type_code,
    is_block_type_heading,
    is_block_type_ordered_list,
    is_block_type_quote,
    is_block_type_unordered_list,
    block_to_block_type,
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
        self.assertEqual(result, "paragraph")

    def test_heading(self):
        text = "# Test"
        result = block_to_block_type(text)
        self.assertEqual(result, "heading")

    def test_code(self):
        text = "```Test\nTest```"
        result = block_to_block_type(text)
        self.assertEqual(result, "code")

    def test_quote(self):
        text = "> Test\n> Test"
        result = block_to_block_type(text)
        self.assertEqual(result, "quote")

    def test_unordered_list(self):
        text = "* Test"
        result = block_to_block_type(text)
        self.assertEqual(result, "unordered_list")

    def test_ordered_list(self):
        text = "1. Test\n2. Test"
        result = block_to_block_type(text)
        self.assertEqual(result, "ordered_list")


if __name__ == "__main__":
    unittest.main()
