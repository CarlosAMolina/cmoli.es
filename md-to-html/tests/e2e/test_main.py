import pathlib
import unittest

from src import main


class TestDirectoryAnalyzer(unittest.TestCase):
    def setUp(self):
        script_dir = pathlib.Path(__file__).parent.absolute()
        tests_dir = script_dir.parent
        self.pathname_to_analyze = pathlib.PurePath(tests_dir, "files", "fake-project")

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
                str(pathlib.PurePath(self.pathname_to_analyze, "folder-1", "foo.md")),
            ],
            md_files,
        )


class TestRun(unittest.TestCase):
    def setUp(self):
        script_dir = pathlib.Path(__file__).parent.absolute()
        tests_dir = script_dir.parent
        self.pathname_to_analyze = pathlib.PurePath(tests_dir, "files", "fake-project")

    def test_run(self):
        css_pathname = str(pathlib.PurePath(self.pathname_to_analyze, "style.css"))
        output_dir_pathname = "/tmp/cmoli.es/html"
        pandoc_template_file_pathname = "pandoc-config/template.html"
        pandoc_metadata_file_pathname = "pandoc-config/metadata.yml"
        main.run(
            css_pathname=css_pathname,
            output_dir_pathname=output_dir_pathname,
            pandoc_metadata_file_pathname=pandoc_metadata_file_pathname,
            pandoc_template_file_pathname=pandoc_template_file_pathname,
            pathname_to_analyze=self.pathname_to_analyze,
        )
