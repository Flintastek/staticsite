import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return

    new = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new.append(node)
        else:
            new_texts = node.text.split(delimiter)
            if len(new_texts)%2 == 0:
                raise Exception("Invalid Markdown syntax")
            for i, text in enumerate(new_texts):
                if i % 2 == 0:
                    new.append(TextNode(text, TextType.TEXT))
                else:
                    new.append(TextNode(text, text_type))
    return new

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            if len(node.text) > 0:
                new.append(node)
        else:
            if len(node.text) > 0:
                images = extract_markdown_images(node.text)
                if not images:
                    new.append(node)
                    continue
                remaining = node.text
                for alt, url in images:
                    part = remaining.split(f"![{alt}]({url})",1)
                    if part[0]:
                        new.append(TextNode(part[0],TextType.TEXT))
                    new.append(TextNode(alt, TextType.IMAGE, url))
                    remaining = part[1]
                if remaining:
                     new.append(TextNode(remaining,TextType.TEXT))

    return new

def split_nodes_link(old_nodes):
    new = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            if len(node.text) > 0:
                new.append(node)
        else:
            if len(node.text) > 0:
                links = extract_markdown_links(node.text)
                if not links:
                    new.append(node)
                    continue
                remaining = node.text
                for text, url in links:
                    part = remaining.split(f"[{text}]({url})",1)
                    if part[0]:
                        new.append(TextNode(part[0],TextType.TEXT))
                    new.append(TextNode(text, TextType.LINK, url))
                    remaining = part[1]
                if remaining:
                     new.append(TextNode(remaining,TextType.TEXT))

    return new


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
