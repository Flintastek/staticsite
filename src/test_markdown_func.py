import unittest
from block_type import block_to_block_type, BlockType
from markdown_func import markdown_to_blocks, markdown_to_html_node, extract_title
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_newlines(self):
        md = "# Header\n\n\n\nNext block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Header", "Next block"])

class TestMarkdownTohtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
class TestExtractTitle(unittest.TestCase):

    def test_header_inside_codebloock(self):
        md = """
```
# detta är min header
jibberish
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_header(self):

        md = """
# detta är min header
jibberish
This is text that _should_ remain
the **same** even with inline stuff
"""
        header = extract_title(md)
        self.assertEqual(header,"detta är min header")
