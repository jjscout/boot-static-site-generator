from path_tools import copy_contents
from generate_page import generate_pages_recursive


def main():
    copy_contents("static", "public")
    generate_pages_recursive(
        "content",
        "template.html",
        "public",
    )


if __name__ == "__main__":
    main()
