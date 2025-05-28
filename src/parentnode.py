from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("a parent node must have a tag")
        
        if self.children == None:
            raise ValueError("a parent node must have children")
        
        result = ""
        for child in self.children:
            result += child.to_html()
        result = f"<{self.tag}>{result}</{self.tag}>"

        return result
