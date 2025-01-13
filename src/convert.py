from block_handling import markdown_to_text_blocks, block_to_html_node
from htmlnode import ParentNode


def convert_markdown_to_html(markdown):
    blocks = markdown_to_text_blocks(markdown)
    html_node = ParentNode("div", [block_to_html_node(block) for block in blocks])
    html = html_node.to_html()
    return html
