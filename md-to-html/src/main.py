import argparse
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
        return (
            self._css_filename
            if css_pathname_without_filename == file_pathname_without_filename
            else self._get_css_relative_pathname_when_files_with_different_paths(
                css_pathname_without_filename,
                file_pathname_without_filename,
            )
        )

    def _get_css_relative_pathname_when_files_with_different_paths(
        self,
        css_pathname_without_filename: pathlib.PurePath,
        file_pathname_without_filename: pathlib.PurePath,
    ) -> str:
        folders_between_files_path: pathlib.PurePath = (
            file_pathname_without_filename.relative_to(css_pathname_without_filename)
        )
        folders_between_files = str(folders_between_files_path).split("/")
        relative_pathnames = [".." for _ in folders_between_files]
        relative_pathname = "/".join(relative_pathnames)
        result = "{}/{}".format(relative_pathname, self._css_filename)
        return result

    @property
    def _css_filename(self) -> str:
        return self._css_path.name


class CommandGenerator:
    def __init__(
        self,
        css_file_pathname: str,
        filename_to_convert: str,
        output_dir_pathname: str,
        pandoc_metadata_file_pathname: str,
        pandoc_template_file_pathname: str,
    ):
        self._css_file_pathname = css_file_pathname
        self._filename_with_extension_to_convert = FilenameWithExtension(
            filename_to_convert
        )
        self._output_dir_pathname = output_dir_pathname
        self._pandoc_metadata_file_pathname = pandoc_metadata_file_pathname
        self._pandoc_template_file_pathname = pandoc_template_file_pathname

    @property
    def command(self) -> str:
        return "./convert-md-to-html {} {} {} {} {}".format(
            self._file_to_convert_pathname,
            self._file_converted_pathname,
            self._css_file_pathname,
            self._pandoc_template_file_pathname,
            self._pandoc_metadata_file_pathname,
        )

    @property
    def _file_to_convert_pathname(self) -> str:
        return "{}/{}".format(
            self._output_dir_pathname, self._filename_with_extension_to_convert.md
        )

    @property
    def _file_converted_pathname(self) -> str:
        return "{}/{}".format(
            self._output_dir_pathname, self._filename_with_extension_to_convert.html
        )


def get_parser():
    parser = argparse.ArgumentParser(
        description="Create script to convert .md files to .html"
    )
    parser.add_argument("css_pathname", type=str)
    parser.add_argument("pandoc_metadata_file_pathname", type=str)
    parser.add_argument("pandoc_template_file_pathname", type=str)
    parser.add_argument("pathname_to_analyze", type=str)
    parser.add_argument("result_file_pathname", type=str)
    return parser


def get_path_substract_common_parts(
    path_1: pathlib.PurePath, path_2: pathlib.PurePath
) -> pathlib.PurePath:
    return path_1.relative_to(path_2)


def run(
    css_pathname: str,
    pandoc_metadata_file_pathname: str,
    pandoc_template_file_pathname: str,
    pathname_to_analyze: str,
    result_file_pathname: str,
):
    print(f"Init export file {result_file_pathname}")
    css_path = pathlib.PurePath(css_pathname)
    css_path_detector = CssPathDetector(css_path)
    with open(result_file_pathname, "w") as f:
        for md_pathname in DirectoryAnalyzer().get_md_pathnames(pathname_to_analyze):
            print(f"Detected .md file: {md_pathname}")
            md_path = pathlib.PurePath(md_pathname)
            css_relative_pathname = (
                css_path_detector.get_css_relative_pathname_from_file_path(md_path)
            )
            pathname_file_to_convert = str(
                get_path_substract_common_parts(
                    md_path, pathlib.PurePath(pathname_to_analyze)
                )
            )
            command = CommandGenerator(
                css_file_pathname=css_relative_pathname,
                filename_to_convert=pathname_file_to_convert,
                output_dir_pathname=pathname_to_analyze,
                pandoc_template_file_pathname=pandoc_template_file_pathname,
                pandoc_metadata_file_pathname=pandoc_metadata_file_pathname,
            ).command
            print(f"Command: {command}")
            f.write(command)
            f.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    run(
        args.css_pathname,
        args.pandoc_metadata_file_pathname,
        args.pandoc_template_file_pathname,
        args.pathname_to_analyze,
        args.result_file_pathname,
    )
