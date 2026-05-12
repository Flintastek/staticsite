from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
import shutil
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # parent of src/
    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")
    # Skapa några olika noder
    node1 = TextNode("Detta är en rubrik", TextType.BOLD, "https://google.se")
    node2 = TextNode("Detta är en rubrik", TextType.BOLD, "https://google.se")
    node3 = TextNode("Lite kod här", TextType.Code, None)

    # Printa ut dem (använder din __repr__)
    print("Mina noder:")
    print(node1)
    print(node2)
    print(node3)

    # Testa om noderna är lika (använder din __eq__)
    print("\nTester:")
    print(f"Är node1 och node2 lika? {node1 == node2}") # Bör vara True
    print(f"Är node1 och node3 lika? {node1 == node3}") # Bör vara False
    
    copy_to_dest(static,public_path,True)
    

def copy_to_dest(src, dest, delete):
    if delete:
        if os.path.exsist(dest):
            shutil.rmtree(dest)
        os.mkdir(dest)

    files = os.listdir(src)
    
    for file in files:
        src_path = os.path.join(src,file)
        if os.path.isfile(src_path):
            shutil.copy(src_path,dest)
        elif os.path.isdir(src_path):
            os.mkdir(os.path.join(dest, file))
            copy_to_dest(src_path, os.path.join(dest, file), False)
        else:
            continue
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text) 
        case TextType.BOLD:
            return LeafNode("b", text_node.text) 
        case TextType.ITALIC:
            return f"<b>{text_node.text}</b>"
        case TextType.CODE:
            return f"<code>{text_node.text}</code>"
        case TextType.LINK:
             return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
             return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise exception("Unknown text type")






if __name__ == "__main__":
    main()
