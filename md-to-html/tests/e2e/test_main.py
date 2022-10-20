import pathlib
import unittest

from src import main


class TestDirectoryAnalyzer(unittest.TestCase):
    def test_get_md_pathnames(self):
        script_dir = pathlib.Path(__file__).parent.absolute()
        pathname_to_analize = pathlib.PurePath(
            script_dir.parent.parent, "tests", "files", "fake-project"
        )
        md_files = [
            pathname
            for pathname in main.DirectoryAnalyzer().get_md_pathnames(
                pathname_to_analize
            )
        ]
        self.assertEqual(
            [
                str(pathlib.PurePath(pathname_to_analize, "foo.md")),
                str(pathlib.PurePath(pathname_to_analize, "folder-1", "foo.md")),
            ],
            md_files,
        )
