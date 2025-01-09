from enum import Enum

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # "html tag"
        self.value = value # "tag text contents"
        self.children = children # [HTMLNode(), HTMLNode()]
        self.props = props # {"attribute":"contents"}

    def __eq__(self, value):
        return str(self) == str(value)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("")
    
    def props_to_html(self):
        props = []
        for key in self.props.keys():
            props.append(f' {key}="{self.props[key]}"')
        return "".join(props)