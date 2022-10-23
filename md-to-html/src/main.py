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
        return str(pathlib.PurePath(self._filename).with_suffix(extension))

    @property
    def md(self) -> str:
        return self._get_filename_with_extension(".md")


class DirectoryAnalyzer:
    def get_md_pathnames(self, pathname: str) -> tp.Iterator[str]:
        print("Init checking", pathname)
        for (dir_pathname, dirnames, filenames) in os.walk(pathname):
            # print(dir_pathname, dirnames, filenames)
            for filename in filenames:
                if FilenameExtensionDetector.is_md(filename):
                    yield str(pathlib.PurePath(dir_pathname, filename))


class CssPathDetector:
    def __init__(self, css_path: pathlib.PurePath):
        self._css_path = css_path

    def get_css_relative_pathname_from_file_path(
        self, file_path: pathlib.PurePath
    ) -> str:
        css_pathname_without_filename = self._css_path.parent
        file_pathname_without_filename = file_path.parent
        folders_between_files_path: pathlib.PurePosixPath = (
            file_pathname_without_filename.relative_to(css_pathname_without_filename)
        )
        folders_between_files = str(folders_between_files_path).split("/")
        relative_pathnames = [".." for _ in folders_between_files]
        relative_pathname = "/".join(relative_pathnames)
        result = "{}/{}".format(relative_pathname, self._css_path.name)
        return result
