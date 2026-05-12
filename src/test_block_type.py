import unittest
from src.block_type import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Level 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        code = r"```" + "\n" + "print('hello')" + "\n" + r"```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        multi_quote = "> Line 1\n> Line 2"
        self.assertEqual(block_to_block_type(multi_quote), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        ulist = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(ulist), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        olist = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(olist), BlockType.ORDERED_LIST)
        bad_olist = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(bad_olist), BlockType.PARAGRAPH)


