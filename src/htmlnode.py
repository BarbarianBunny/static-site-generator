from enum import Enum


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # "html tag"
        self.value = value  # "tag text contents"
        self.children = children  # [HTMLNode(), HTMLNode()]
        self.props = props  # {"attribute":"contents"}

    def __eq__(self, value):
        return str(self) == str(value)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_list = []
        for key in self.props.keys():
            props_list.append(f' {key}="{self.props[key]}"')
        return "".join(props_list)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return str(self.value)
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Invalid HTML: no children")
        return (
            f"<{self.tag}{self.props_to_html()}>{self.children_to_html()}</{self.tag}>"
        )

    def children_to_html(self):
        if self.children is None:
            return ""
        return "".join([child.to_html() for child in self.children])
