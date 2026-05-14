class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag=tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        print("tag:",self.tag)
        print("value:",self.value)
        print("children:",self.children)
        print("props:",self.props)

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return "" 
        html=""
        for key,value in self.props.items():
            html += f' {key}="{value}"'
        return html
        
class LeafNode(HTMLNode):
    def __init__(self,tag,value=None,props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        print("tag:",self.tag)
        print("value:",self.value)
        print("props:",self.props)

class ParentNode(HTMLNode):
    def __init__(self,tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("no children!")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
