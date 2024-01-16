import argparse
import logging
import os
import pathlib
import typing as tp
import sys


class Logger:
    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        logger.addHandler(self._console_handler)
        logger.addHandler(self._file_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    @property
    def _console_handler(self):
        c_handler = logging.StreamHandler(sys.stdout)
        c_format = logging.Formatter(self._log_format, datefmt=self._date_format)
        c_handler.setFormatter(c_format)
        return c_handler

    @property
    def _file_handler(self):
        f_handler = logging.FileHandler(filename=self._log_file_pathname, mode="w")
        f_format = logging.Formatter(self._log_format, datefmt=self._date_format)
        f_handler.setFormatter(f_format)
        return f_handler

    @property
    def _log_file_pathname(self) -> str:
        current_dir_pathname = pathlib.Path(__file__).parent.absolute()
        result = current_dir_pathname.joinpath("file.log")
        result = str(result)
        return result

    @property
    def _log_format(self) -> str:
        return "%(asctime)s - %(levelname)s - %(message)s"

    @property
    def _date_format(self) -> str:
        return "%Y-%m-%d %H:%M:%S"


logger = Logger().logger


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


def os_walk_exception_handler(exception_instance):
    raise exception_instance


class DirectoryAnalyzer:
    def get_md_pathnames(self, pathname: str) -> tp.Iterator[str]:
        logger.debug(f"Init checking {pathname}")
        for (dir_pathname, dirnames, filenames) in os.walk(
            pathname, onerror=os_walk_exception_handler
        ):
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
        output_directory_pathname: str,
        pandoc_metadata_file_pathname: str,
        pandoc_script_convert_md_to_html_file_pathname: str,
        pandoc_template_file_pathname: str,
    ):
        self._css_file_pathname = css_file_pathname
        self._filename_with_extension_to_convert = FilenameWithExtension(
            filename_to_convert
        )
        self._output_directory_pathname = output_directory_pathname
        self._pandoc_metadata_file_pathname = pandoc_metadata_file_pathname
        self._pandoc_script_convert_md_to_html_file_pathname = (
            pandoc_script_convert_md_to_html_file_pathname
        )
        self._pandoc_template_file_pathname = pandoc_template_file_pathname

    @property
    def command(self) -> str:
        return "/bin/sh {} {} {} {} {} {}".format(
            self._pandoc_script_convert_md_to_html_file_pathname,
            self._file_to_convert_pathname,
            self._file_converted_pathname,
            self._css_file_pathname,
            self._pandoc_template_file_pathname,
            self._pandoc_metadata_file_pathname,
        )

    @property
    def _file_to_convert_pathname(self) -> str:
        return "{}/{}".format(
            self._output_directory_pathname, self._filename_with_extension_to_convert.md
        )

    @property
    def _file_converted_pathname(self) -> str:
        return "{}/{}".format(
            self._output_directory_pathname,
            self._filename_with_extension_to_convert.html,
        )


def get_parser():
    parser = argparse.ArgumentParser(
        description="Create script to convert .md files to .html"
    )
    parser.add_argument("css_pathname", type=str)
    parser.add_argument("pandoc_metadata_file_pathname", type=str)
    parser.add_argument("pandoc_script_convert_md_to_html_file_pathname", type=str)
    parser.add_argument("pandoc_template_file_pathname", type=str)
    parser.add_argument("pathname_to_analyze", type=str)
    parser.add_argument("result_file_pathname", type=str)
    return parser


def get_path_substract_common_parts(
    path_1: pathlib.PurePath, path_2: pathlib.PurePath
) -> pathlib.PurePath:
    return path_1.relative_to(path_2)


# TODO add to run()
def export_to_file_the_md_pathnames_to_convert(
    pathname_to_analyze: str,
    result_file_pathname: str,
):
    logger.debug(f"Init export file {result_file_pathname}")
    with open(result_file_pathname, "w") as f:
        for md_pathname in DirectoryAnalyzer().get_md_pathnames(pathname_to_analyze):
            logger.debug(f"Detected .md file: {md_pathname}")
            f.write(md_pathname)
            f.write("\n")


# TODO add to run()
def export_to_file_the_html_pathnames_converted(
    analized_directory_pathname: str,
    md_pathnames_to_convert_file_pathname: str,
    output_directory_pathname: str,
    result_file_pathname: str,
):
    logger.debug(f"Init export file {result_file_pathname}")
    with open(md_pathnames_to_convert_file_pathname, "r") as f_to_read, open(
        result_file_pathname, "w"
    ) as f_to_write:
        for file_to_convert_pathname in f_to_read.read().splitlines():
            logger.debug(f"Pathname to convert: {file_to_convert_pathname}")
            pathname_converted = get_pathname_converted(
                analized_directory_pathname,
                file_to_convert_pathname,
                output_directory_pathname,
            )
            logger.debug(f"Pathname converted: {pathname_converted}")
            f_to_write.write(pathname_converted)
            f_to_write.write("\n")


def get_pathname_converted(
    analized_directory_pathname: str,
    file_to_convert_pathname: str,
    output_directory_pathname: str,
) -> str:
    path_to_convert = pathlib.PurePath(file_to_convert_pathname)
    path_to_convert_without_analized_path = get_path_substract_common_parts(
        path_to_convert, pathlib.PurePath(analized_directory_pathname)
    )
    filename_to_convert = path_to_convert.name
    filename_converted = FilenameWithExtension(filename_to_convert).html
    path_converted_without_analized_path = (
        path_to_convert_without_analized_path.with_name(filename_converted)
    )
    path_converted = pathlib.PurePath(output_directory_pathname).joinpath(
        path_converted_without_analized_path,
    )
    pathname_converted = str(path_converted)
    return pathname_converted


# TODO add to run()
def export_to_file_the_css_relative_pathnames(
    css_pathname: str,
    md_pathnames_to_convert_file_pathname: str,
    result_file_pathname: str,
):
    logger.debug(f"Init export file {result_file_pathname}")
    css_path = pathlib.PurePath(css_pathname)
    css_path_detector = CssPathDetector(css_path)
    with open(md_pathnames_to_convert_file_pathname, "r") as f_to_read, open(
        result_file_pathname, "w"
    ) as f_to_write:
        for file_to_convert_pathname in f_to_read.read().splitlines():
            logger.debug(f"Pathname to convert: {file_to_convert_pathname}")
            file_to_convert_path = pathlib.PurePath(file_to_convert_pathname)
            css_relative_pathname = (
                css_path_detector.get_css_relative_pathname_from_file_path(
                    file_to_convert_path
                )
            )
            logger.debug(f"Css relative pathname: {css_relative_pathname}")
            f_to_write.write(css_relative_pathname)
            f_to_write.write("\n")


def run(
    css_pathname: str,
    pandoc_metadata_file_pathname: str,
    pandoc_script_convert_md_to_html_file_pathname: str,
    pandoc_template_file_pathname: str,
    pathname_to_analyze: str,
    result_file_pathname: str,
):
    logger.debug(f"Init export file {result_file_pathname}")
    css_path = pathlib.PurePath(css_pathname)
    css_path_detector = CssPathDetector(css_path)
    with open(result_file_pathname, "w") as f:
        for md_pathname in DirectoryAnalyzer().get_md_pathnames(pathname_to_analyze):
            logger.debug(f"Detected .md file: {md_pathname}")
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
                output_directory_pathname=pathname_to_analyze,
                pandoc_metadata_file_pathname=pandoc_metadata_file_pathname,
                pandoc_script_convert_md_to_html_file_pathname=pandoc_script_convert_md_to_html_file_pathname,
                pandoc_template_file_pathname=pandoc_template_file_pathname,
            ).command
            logger.debug(f"Command: {command}")
            f.write(command)
            f.write("\n")


if __name__ == "__main__":
    args = get_parser().parse_args()
    run(
        args.css_pathname,
        args.pandoc_metadata_file_pathname,
        args.pandoc_script_convert_md_to_html_file_pathname,
        args.pandoc_template_file_pathname,
        args.pathname_to_analyze,
        args.result_file_pathname,
    )
