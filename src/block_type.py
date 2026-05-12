from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"    

def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING

    if re.match(r"^`{3}\n.*`{3}$", markdown, re.DOTALL):
        return BlockType.CODE
    lines = markdown.split('\n')
    if markdown.startswith(">"):
        is_quote = True
        for line in lines:
            if not line.startswith(">"):
                is_quote = False
        if is_quote:
            return BlockType.QUOTE

    if markdown.startswith("- "):
        is_ulist = True
        for line in lines:
            if not line.startswith("- "):
                is_ulist = False
        if is_ulist:
            return BlockType.UNORDERED_LIST

    is_ordered = True
    for i in range(len(lines)):
        expected_start = f"{i+1}. "
        if not lines[i].startswith(expected_start):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
