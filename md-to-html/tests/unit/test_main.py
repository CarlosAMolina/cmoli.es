import pathlib
import unittest

from src import main


class TestFilenameExtensionDetector(unittest.TestCase):
    def test_is_md_is_true(self):
        self.assertTrue(main.FilenameExtensionDetector.is_md("foo.md"))

    def test_is_md_is_false(self):
        self.assertFalse(main.FilenameExtensionDetector.is_md("foo.html"))


class TestFilenameWithExtension(unittest.TestCase):
    def setUp(self):
        filename = "foo.md"
        self.filename_with_extension = main.FilenameWithExtension(filename)

    def test_html(self):
        self.assertEqual("foo.html", self.filename_with_extension.html)

    def test_md(self):
        self.assertEqual("foo.md", self.filename_with_extension.md)


class TestCssPathDetector(unittest.TestCase):
    def test_get_css_relative_pathname_from_file_path(self):
        css_path = pathlib.PurePath("/foo/bar/foo.css")
        html_path = pathlib.PurePath("/foo/bar/folder_1/folder_2/index.html")
        css_path_detector = main.CssPathDetector(css_path)
        self.assertEqual(
            "../../foo.css",
            css_path_detector.get_css_relative_pathname_from_file_path(html_path),
        )

    def test_get_css_relative_pathname_from_file_path_if_files_in_same_path(self):
        css_path = pathlib.PurePath("/foo/bar/foo.css")
        html_path = pathlib.PurePath("/foo/bar/index.html")
        css_path_detector = main.CssPathDetector(css_path)
        self.assertEqual(
            "foo.css",
            css_path_detector.get_css_relative_pathname_from_file_path(html_path),
        )
