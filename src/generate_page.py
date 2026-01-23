import os
from markdown_blocks import markdown_to_html_node
from markdown_tools import extract_title


def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise OSError(f"{from_path} not found")
    if not os.path.exists(template_path):
        raise OSError(f"{template_path} not found")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        text = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(text).to_html()
    page = template.replace("{{ Title }}", extract_title(text))
    page = page.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path,
):
    os.makedirs(dest_dir_path, exist_ok=True)
    for item in os.listdir(dir_path_content):
        itempath = os.path.join(dir_path_content, item)
        destpath = os.path.join(dest_dir_path, item)
        print(item, itempath)
        if os.path.isfile(itempath) and itempath[-3:] == ".md":
            generate_page(
                itempath,
                template_path,
                destpath.replace("md", "html"),
            )
            continue
        generate_pages_recursive(
            itempath,
            template_path,
            destpath,
        )
