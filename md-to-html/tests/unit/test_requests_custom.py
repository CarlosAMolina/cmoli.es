import unittest

from src import main


class TestFilenameWithExtension(unittest.TestCase):
    def setUp(self):
        filename = "foo.md"
        self.filename_with_extension = main.FilenameWithExtension(filename)

    def test_html(self):
        self.assertEqual("foo.html", self.filename_with_extension.html)

    def test_md(self):
        self.assertEqual("foo.md", self.filename_with_extension.md)
