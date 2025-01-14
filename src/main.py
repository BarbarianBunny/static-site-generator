import os
from static_to_public import static_to_public
from template import generate_page


def main():
    static_to_public()
    from_path = os.path.join(os.getcwd(), "content", "index.md")
    template_path = os.path.join(os.getcwd(), "template.html")
    dest_path = os.path.join(os.getcwd(), "public", "index.html")

    generate_page(from_path, template_path, dest_path)


main()
