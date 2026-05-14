from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_func import markdown_to_html_node, extract_title
import os
import sys
import shutil
def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # parent of src/
    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "docs")
    content_path= os.path.join(project_root, "content")
    
    copy_to_dest(static_path,public_path,True)
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive(content_path, "template.html", public_path, basepath)
    

def copy_to_dest(src, dest, delete):
    if delete:
        if os.path.exists(dest):
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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Conjure up page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_contents = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        temp= f.read()

    html_node = markdown_to_html_node(markdown_contents)
    html_string = html_node.to_html()
    page_title = extract_title(markdown_contents)
    html_page = temp.replace("{{ Title }}", page_title)
    html_page = html_page.replace("{{ Content }}", html_string)
    html_page = html_page.replace('href="/', f'href="{basepath}')
    html_page = html_page.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)

    for file in files:
        src_path = os.path.join(dir_path_content,file)
        if os.path.isfile(src_path) and file.endswith(".md"):
            html_filename = file.replace(".md", ".html")
            generate_page(src_path, template_path, os.path.join(dest_dir_path,html_filename), basepath)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, os.path.join(dest_dir_path, file), basepath)
        else:
            continue
    

if __name__ == "__main__":
    main()
