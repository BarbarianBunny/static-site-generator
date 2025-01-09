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

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return str(self) == str(value)
    
    def __repr__(self):
        return f"TextNode(\"{self.text}\", {self.text_type.value}, \"{self.url}\")"

    def to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.LINK:
                if text_node.url is None:
                    raise ValueError("Invalid LINK: no url")
                return LeafNode(str(text_node.text_type), text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                if text_node.url is None:
                    raise ValueError("Invalid IMAGE: no src url")
                return LeafNode(str(text_node.text_type), "", {"src": text_node.url, "alt": text_node.text})

        return LeafNode(str(text_node.text_type), text_node.text)
