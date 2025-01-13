import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode


class BlockType(Enum):
    def __str__(self):
        return str(self.value)

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_text_blocks(markdown):
    blocks_regex = re.compile(r"(?:[^\n\s]+?.+\n?)+")
    matched_blocks = blocks_regex.findall(markdown)
    blocks = [block.strip() for block in matched_blocks]
    return blocks


def block_to_block_type(text) -> BlockType:
    if is_block_type_heading(text):
        return BlockType.HEADING
    if is_block_type_code(text):
        return BlockType.CODE
    if is_block_type_quote(text):
        return BlockType.QUOTE
    if is_block_type_unordered_list(text):
        return BlockType.UNORDERED_LIST
    if is_block_type_ordered_list(text):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)


def paragraph_to_html_node(block):
    return ParentNode("p", TextNode(block, TextType.TEXT).to_html_nodes())


def heading_to_html_node(block):
    heading_regex = re.compile(r"(^#+ )[^\n]+$")
    hashes = heading_regex.findall(block)
    hash_count = hashes[0].count("#")
    text = block[hash_count + 1 :]
    return ParentNode(f"h{hash_count}", TextNode(text, TextType.TEXT).to_html_nodes())


def code_to_html_node(block):
    code_regex = re.compile(r"^```([^`]+)```$")
    text = code_regex.findall(block)[0]
    return ParentNode("pre", TextNode(text, TextType.CODE).to_html_nodes())


def quote_to_html_node(block):
    quote_regex = re.compile(r"> ?(.+)")
    text_list = quote_regex.findall(block)
    text = "\n".join(text_list)
    return ParentNode("blockquote", TextNode(text, TextType.TEXT).to_html_nodes())


def unordered_list_to_html_node(block):
    unordered_regex = re.compile(r"[\*-] (.*)\n*")
    text_list = unordered_regex.findall(block)
    list_items = [
        ParentNode("li", TextNode(text, TextType.TEXT).to_html_nodes())
        for text in text_list
    ]
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    unordered_regex = re.compile(r"\d+\. (.*)\n*")
    text_list = unordered_regex.findall(block)
    list_items = [
        ParentNode("li", TextNode(text, TextType.TEXT).to_html_nodes())
        for text in text_list
    ]
    return ParentNode("ol", list_items)


def is_block_type_heading(text):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    heading_regex = re.compile(r"(^#+ )[^\n]+$")
    hashes = heading_regex.findall(text)
    if len(hashes) != 1:
        return False
    hash_count = hashes[0].count("#")
    if hash_count <= 0 or hash_count > 6:
        return False
    return True


def is_block_type_code(text):
    # Code blocks must start with 3 backticks and end with 3 backticks.
    code_regex = re.compile(r"^```[^`]+```$")
    match = code_regex.fullmatch(text)
    return match != None


def is_block_type_quote(text):
    # Every line in a quote block must start with a > character.
    quote_regex = re.compile(r"^(?:>.*\n*)+$")
    match = quote_regex.fullmatch(text)
    return match != None


def is_block_type_unordered_list(text):
    # Every line in an unordered list block must start with a * or - character, followed by a space.
    unordered_regex = re.compile(r"^(?:[\*-] .*\n*)+$")
    match = unordered_regex.fullmatch(text)
    return match != None


def is_block_type_ordered_list(text):
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    unordered_regex = re.compile(r"^(?:\d+\. .*\n*)+$")
    match = unordered_regex.fullmatch(text)
    if match == None:
        return False
    unordered_regex = re.compile(r"(\d+?)\. .*\n*")
    matches = unordered_regex.findall(text)
    ordered_number = 1
    for number in matches:
        if int(number) != ordered_number:
            return False
        ordered_number += 1
    return True
