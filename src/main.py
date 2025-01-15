import os
from static_to_public import static_to_public
from template import generate_pages_recursively


def main():
    static_to_public()

    from_content = os.path.join(os.getcwd(), "content")
    template_path = os.path.join(os.getcwd(), "template.html")
    dest_public = os.path.join(os.getcwd(), "public")

    generate_pages_recursively(from_content, template_path, dest_public)


main()
