from distutils import dir_util
import pathlib
import unittest

from src import main


class TestDirectoryAnalyzer(unittest.TestCase):
    def setUp(self):
        script_dir = pathlib.Path(__file__).parent.absolute()
        tests_dir = script_dir.parent
        self.pathname_to_analyze = str(
            pathlib.PurePath(tests_dir, "files", "fake-project")
        )

    def test_get_md_pathnames(self):
        md_files = [
            pathname
            for pathname in main.DirectoryAnalyzer().get_md_pathnames(
                self.pathname_to_analyze
            )
        ]
        self.assertEqual(
            [
                str(pathlib.PurePath(self.pathname_to_analyze, "foo.md")),
                str(pathlib.PurePath(self.pathname_to_analyze, "folder-1", "bar.md")),
            ],
            md_files,
        )

    def test_exception_is_raised_if_pathname_to_analyze_does_not_exist(self):
        pathname_to_analyze = "/foo/bar/asdf/foo/bar"
        with self.assertRaises(FileNotFoundError):
            for _ in main.DirectoryAnalyzer().get_md_pathnames(pathname_to_analyze):
                pass


class TestRun(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None # Show complete diff when test fails.
        script_dir = pathlib.Path(__file__).parent.absolute()
        tests_dir = script_dir.parent
        self.pathname_to_analyze = "/tmp/cmoli.es/html"
        pathname_with_files_to_analyze = str(
            pathlib.PurePath(tests_dir, "files", "fake-project")
        )
        dir_util.copy_tree(pathname_with_files_to_analyze, self.pathname_to_analyze)

    def test_run(self):
        css_pathname = str(pathlib.PurePath(self.pathname_to_analyze, "style.css"))
        pandoc_metadata_file_pathname = "pandoc-config/metadata.yml"
        pandoc_script_convert_md_to_html_file_pathname = "convert-md-to-html"
        pandoc_template_file_pathname = "pandoc-config/template.html"
        result_file_pathname = "/tmp/md-to-html"
        main.run(
            css_pathname=css_pathname,
            pandoc_metadata_file_pathname=pandoc_metadata_file_pathname,
            pandoc_script_convert_md_to_html_file_pathname=pandoc_script_convert_md_to_html_file_pathname,
            pandoc_template_file_pathname=pandoc_template_file_pathname,
            pathname_to_analyze=self.pathname_to_analyze,
            result_file_pathname=result_file_pathname,
        )
        with open(result_file_pathname, "r") as f:
            result = f.read()
        expected_result = "{}\n{}\n".format(
        "/bin/sh convert-md-to-html /tmp/cmoli.es/html/foo.md /tmp/cmoli.es/html/foo.html style.css pandoc-config/template.html pandoc-config/metadata.yml",
        "/bin/sh convert-md-to-html /tmp/cmoli.es/html/folder-1/bar.md /tmp/cmoli.es/html/folder-1/bar.html ../style.css pandoc-config/template.html pandoc-config/metadata.yml")
        self.assertEqual(expected_result, result)
