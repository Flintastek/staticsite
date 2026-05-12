import unittest
import re
from node_utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("Detta är `kod` här", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Detta är ", TextType.TEXT),
            TextNode("kod", TextType.CODE),
            TextNode(" här", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        node = TextNode("Här är **fet** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Här är ", TextType.TEXT),
            TextNode("fet", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_exception_unclosed(self):
        node = TextNode("Detta är `trasig kod", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "Invalid Markdown syntax")

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Redan fet", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Normal text")

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_images(self):
        text = "Här är en bild ![alt text](https://imgur.com) och en till ![katt](https://katter.se)"
        matches = extract_markdown_images(text)
        expected = [
            ("alt text", "https://imgur.com"),
            ("katt", "https://katter.se")
        ]
        self.assertEqual(matches, expected)

    def test_extract_links(self):
        text = "Kolla in [min blogg](https://blogg.se) eller [google](https://google.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("min blogg", "https://blogg.se"),
            ("google", "https://google.com")
        ]
        self.assertEqual(matches, expected)

    def test_links_not_matching_images(self):
        text = "Här är en ![bild](img.png) och en [länk](link.com)"
        matches = extract_markdown_links(text)
        expected = [("länk", "link.com")]
        self.assertEqual(matches, expected)

    def test_images_not_matching_links(self):
        text = "Här är en ![bild](img.png) och en [länk](link.com)"
        matches = extract_markdown_images(text)
        expected = [("bild", "img.png")]
        self.assertEqual(matches, expected)


class TestSplitFunctions(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("Texten slutar med en [länk](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Texten slutar med en ")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)

    def test_split_links_multiple(self):
        node = TextNode(
            "Kolla [Google](https://google.com) och [Bing](https://bing.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Kolla ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" och ", TextType.TEXT),
            TextNode("Bing", TextType.LINK, "https://bing.com"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_no_links(self):
        node = TextNode("Bara vanlig text utan länkar", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Bara vanlig text utan länkar")

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("Länk: [A](url)", TextType.TEXT),
            TextNode("Redan fet", TextType.BOLD),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(len(new_nodes), 3) 
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)

class TestTextToTextNodes(unittest.TestCase):
    def test_integration_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://imgur.com) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://imgur.com"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected)

    def test_integration_simple(self):
        text = "Bara vanlig text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Bara vanlig text", TextType.TEXT)]
        self.assertListEqual(nodes, expected)

    def test_integration_only_formatting(self):
        text = "**BOLD**`CODE`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("BOLD", TextType.BOLD),
            TextNode("CODE", TextType.CODE),
        ]
        self.assertListEqual(nodes, expected)
