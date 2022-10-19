import pathlib


class FilenameExtensionDetector:
    @staticmethod
    def is_md(filename: str) -> bool:
        return pathlib.PurePosixPath(filename).suffix == ".md"


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
