import re
from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    def __str__(self):
        return str(self.value)

    TEXT = ""
    LINK = "a"
    BOLD = "b"
    CODE = "code"
    ITALIC = "i"
    IMAGE = "img"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return str(self) == str(value)

    def __repr__(self):
        return f'TextNode("{self.text}", {self.text_type.value}, "{self.url}")'

    def to_html_node(self):
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.LINK:
                if self.url is None:
                    raise ValueError("Invalid LINK: no url")
                return LeafNode(str(self.text_type), self.text, {"href": self.url})
            case TextType.IMAGE:
                if self.url is None:
                    raise ValueError("Invalid IMAGE: no src url")
                return LeafNode(
                    str(self.text_type), "", {"src": self.url, "alt": self.text}
                )
        return LeafNode(str(self.text_type), self.text)

    def extract_text_nodes(self):
        """Seperates TextNode's text into a list of categorized TextNodes according to Markdown."""
        nodes = split_nodes_delimiter([self])
        return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_texts = old_node.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise ValueError(
                f'Invalid Markdown: Odd count of "{delimiter}" in "{old_node.text}"'
            )
        for i in range(len(split_texts)):
            if split_texts[i] == "":
                continue
            if i % 2 == 0:  # even index
                new_nodes.append(TextNode(split_texts[i], old_node.text_type))
            else:
                new_nodes.append(TextNode(split_texts[i], text_type))
    return new_nodes


def split_nodes_images(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        image_tuples = extract_markdown_images(old_node.text)
        old_text = old_node.text
        for image in image_tuples:
            split_on_image = old_text.split(f"![{image[0]}]({image[1]})")
            if split_on_image == []:
                continue
            old_text = split_on_image[1]
            new_nodes.append(TextNode(split_on_image[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

        if old_text == "":
            continue
        new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        link_tuples = extract_markdown_links(old_node.text)
        old_text = old_node.text
        for link in link_tuples:
            split_on_link = old_text.split(f"[{link[0]}]({link[1]})")
            if split_on_link == []:
                continue
            old_text = split_on_link[1]
            new_nodes.append(TextNode(split_on_link[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if old_text == "":
            continue
        new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    image_regex = re.compile(r"!\[(.*?)\]\((.*?)\)")
    return image_regex.findall(text)


def extract_markdown_links(text):
    image_regex = re.compile(r"[^!]\[(.*?)\]\((.*?)\)")
    return image_regex.findall(text)
