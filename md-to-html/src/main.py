import os
import pathlib
import typing as tp


class FilenameExtensionDetector:
    @staticmethod
    def is_md(filename: str) -> bool:
        return pathlib.PurePath(filename).suffix == ".md"


class FilenameWithExtension:
    def __init__(self, filename: str):
        self._filename = filename

    @property
    def html(self) -> str:
        return self._get_filename_with_extension(".html")

    def _get_filename_with_extension(self, extension: str) -> str:
        return str(pathlib.Path(self._filename).with_suffix(extension))

    @property
    def md(self) -> str:
        return self._get_filename_with_extension(".md")


class DirectoryAnalyzer:
    def get_md_pathnames(self, path: str) -> tp.Iterator[str]:
        for (dir_pathname, dirnames, filenames) in os.walk(path):
            print(dir_pathname, dirnames, filenames)
            for filename in filenames:
                if FilenameExtensionDetector.is_md(filename):
                    yield str(pathlib.PurePath(dir_pathname, filename))


if __name__ == "__main__":
    # TODO move code to e2e test
    script_dir = pathlib.Path(__file__).parent.absolute()
    dir_to_analize = pathlib.PurePath(script_dir.parent.parent, "src")
    for pathname in DirectoryAnalyzer().get_md_pathnames(dir_to_analize):
        print(pathname)
