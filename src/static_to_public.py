import os
import shutil


def static_to_public():
    clear_public_folder()
    copy_static_to_public()
    # Logging the path of each file you copy, so you can see what's happening as you run and debug your code.
    return None


def clear_public_folder():
    """Clears the public folder and returns that it exists"""
    path = os.path.join(os.getcwd(), "public")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    return None


def copy_static_to_public():
    static = os.path.join(os.getcwd(), "static")
    public = os.path.join(os.getcwd(), "public")

    if not os.path.exists(static):
        raise Exception("Static folder doesn't exist")
    if not os.path.exists(public):
        raise Exception("Public folder doesn't exist")

    shutil.copytree(static, public, dirs_exist_ok=True)
    return None
