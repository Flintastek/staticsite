import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        expected = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_single(self):
        node = HTMLNode(props={"class": "primary"})
        self.assertEqual(node.props_to_html(), ' class="primary"')

    def test_values_set_correctly(self):
        node = HTMLNode(tag="p", value="Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_diff_tags(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertNotEqual(node.tag, "lol")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_hmtl_no_children(self):
        parent_node = ParentNode("span", None)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertEqual(str(cm.exception), "no children!")
        
if __name__ == "__main__":
    unittest.main()
