from block_type import block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode
from textnode import TextType
from node_utils import text_to_textnodes 
def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    blocks = []
    for block in markdown_blocks:
        tmp = block.strip()
        if tmp != "":
            blocks.append(tmp)
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = len(re.match(r"#{1,6}", block).group())
            content = block[level:].strip()
            children.append(ParentNode(f"h{level}", text_to_children(content)))
        elif block_type == BlockType.CODE:
            content = block.strip("`").strip()
            code_leaf = LeafNode("code", content)
            children.append(ParentNode("pre", [code_leaf]))
        elif block_type == BlockType.QUOTE:
            content = " ".join([l.lstrip("> ").strip() for l in block.split("\n")])
            children.append(ParentNode("blockquote", text_to_children(content)))
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                content = line[2:].strip()
                items.append(ParentNode("li", text_to_children(content)))
            children.append(ParentNode("ul", items))
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                content = re.sub(r"^\d+\. ", "", line).strip()
                items.append(ParentNode("li", text_to_children(content)))
            children.append(ParentNode("ol", items))

        else:
            clean_content = block.strip().replace("\n", " ")
            children.append(ParentNode("p", text_to_children(clean_content)))

    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            children.append(LeafNode(None, text_node.text))
        elif text_node.text_type == TextType.BOLD:
            children.append(LeafNode("b", text_node.text))
        elif text_node.text_type == TextType.ITALIC:
            children.append(LeafNode("i", text_node.text))
        elif text_node.text_type == TextType.CODE:
            children.append(LeafNode("code", text_node.text))
        elif text_node.text_type == TextType.LINK:
            children.append(LeafNode("a", text_node.text, {"href": text_node.url}))
        elif text_node.text_type == TextType.IMAGE:
            children.append(LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}))
    return children
