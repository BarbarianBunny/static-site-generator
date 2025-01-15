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


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    contents = os.scandir(dir_path_content)
    for content in contents:
        path_end = os.path.split(content.path)[1]
        if content.is_dir():
            # dir_path_content = /workspace/github.com/BarbarianBunny/static-site-generator/content
            # dest_dir_path = /workspace/github.com/BarbarianBunny/static-site-generator/public
            # content.path = /workspace/github.com/BarbarianBunny/static-site-generator/content/majesty
            # pum = /workspace/github.com/BarbarianBunny/static-site-generator/public/majesty
            new_dest_dir_path = os.path.join(dest_dir_path, path_end)
            generate_pages_recursively(content.path, template_path, new_dest_dir_path)
            continue
        if content.is_file() and is_markdown_file(content.path):
            path, ext = os.path.splitext(path_end)
            html_path = f"{path}.html"
            dest_path = os.path.join(dest_dir_path, html_path)
            generate_page(content.path, template_path, dest_path)
    return None


def is_markdown_file(path):
    return path.endswith(".md") or path.endswith(".markdown")
