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
