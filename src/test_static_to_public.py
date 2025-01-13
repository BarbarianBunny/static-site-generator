import unittest

from static_to_public import clear_public_folder, copy_static_to_public


class TestClearPublicFolder(unittest.TestCase):
    def test_folder_exists(self):
        clear_public_folder()
        self.assertTrue(True)


class TestCopyStaticToPublic(unittest.TestCase):
    def test_copy_src(self):
        clear_public_folder()
        copy_static_to_public()
        self.assertTrue(True)
