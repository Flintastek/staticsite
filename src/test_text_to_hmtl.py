import unittest
from main import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_conversion(self):
        # Test för fetstil
        node = TextNode("Fet text", TextType.BOLD, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Fet text")

    def test_link_conversion(self):
        # Test för länk (anchor text + href)
        node = TextNode("Klicka här", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Klicka här")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image_conversion(self):
        # Test för bild (src + alt)
        node = TextNode("Beskrivning", TextType.IMAGE, "bild.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "bild.png", "alt": "Beskrivning"})
