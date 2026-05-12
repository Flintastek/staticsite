import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.ITALIC, None)
        self.assertNotEqual(node, node2)
    def test_url_diff(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url1.se")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://url2.se")
        self.assertNotEqual(node, node2)

        

if __name__ == "__main__":
    unittest.main()
