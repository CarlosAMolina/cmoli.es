import pathlib
import unittest

from src import main


class TestFilenameExtensionDetector(unittest.TestCase):
    def test_is_md_is_true(self):
        self.assertTrue(main.FilenameExtensionDetector.is_md("foo.md"))

    def test_is_md_is_false(self):
        self.assertFalse(main.FilenameExtensionDetector.is_md("foo.html"))


class TestFunctions(unittest.TestCase):
    def test_get_convered_pathname(self):
        result = main.get_pathname_converted(
            analized_directory_pathname="/home/files",
            file_to_convert_pathname="/home/files/folder/foo.html",
            output_directory_pathname="/tmp/html",
        )
        self.assertEqual("/tmp/html/folder/foo.html", result)

    def test_get_filename_set_extension(self):
        filename = "foo.md"
        result = main.get_filename_set_extension(filename, ".html")
        self.assertEqual("foo.html", result)
        self.assertTrue(isinstance(result, str))


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
