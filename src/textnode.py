from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return str(self) == str(value)
    
    def __repr__(self):
        return f"TextNode(\"{self.text}\", {self.text_type.value}, \"{self.url}\")"