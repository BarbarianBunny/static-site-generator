import unittest

from template import extract_title
from template import convert_markdown_to_html


class TestExtractTitle(unittest.TestCase):
    def test_0(self):
        text = "## Test\nTest"
        with self.assertRaises(Exception):
            extract_title(text)

    def test_1(self):
        text = "# Test\n## Test"
        self.assertEqual(extract_title(text), "Test")

    def test_2(self):
        text = "# Test\n# Test"
        with self.assertRaises(Exception):
            extract_title(text)


class TestConvertMarkdownToHTML(unittest.TestCase):
    def test_p(self):
        html = convert_markdown_to_html("Test")
        self.assertEqual(html, "<div><p>Test</p></div>")

    def test_everything(self):
        html = convert_markdown_to_html(
            "Paragraph\n\n* Unorder\n- Unorder\n\n1. Order\n2. Order\n\n```Code```\n\n> Quote\n>Quote\n\n**Bold**\n\n# Header"
        )
        self.assertEqual(
            html,
            "<div><p>Paragraph</p><ul><li>Unorder</li><li>Unorder</li></ul><ol><li>Order</li><li>Order</li></ol><pre><code>Code</code></pre><blockquote>Quote\nQuote</blockquote><p><b>Bold</b></p><h1>Header</h1></div>",
        )
