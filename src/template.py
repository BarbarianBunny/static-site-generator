"""Template functions"""

import re
import os

from block_handling import markdown_to_text_blocks, block_to_html_node
from htmlnode import ParentNode


def extract_title(markdown):
    title_regex = re.compile(r"(?m)^# (.+)")
    titles = title_regex.findall(markdown)
    if len(titles) != 1:
        raise Exception("Title was not found")
    return titles[0]


def convert_markdown_to_html(markdown):
    blocks = markdown_to_text_blocks(markdown)
    html_node = ParentNode("div", [block_to_html_node(block) for block in blocks])
    html = html_node.to_html()
    return html


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page \nfrom:  {from_path} \nto:    {dest_path} \nusing: {template_path}"
    )

    if not os.path.exists(from_path):
        raise Exception(f"Missing From: {from_path}")
    if not os.path.exists(template_path):
        raise Exception(f"Missing Template: {template_path}")
    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    markdown = ""
    with open(from_path, "r") as file:
        markdown = file.read()

    template = ""
    with open(template_path, "r") as file:
        template = file.read()

    title = extract_title(markdown)
    content = convert_markdown_to_html(markdown)
    title_string = "{{ Title }}"
    content_string = "{{ Content }}"

    template = title.join(template.split(title_string))
    template = content.join(template.split(content_string))

    with open(dest_path, "w+") as file:
        file.write(template)
    return None
