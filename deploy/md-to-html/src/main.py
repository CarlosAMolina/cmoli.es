import argparse
import os
import pathlib
import typing as tp

from .logger import Logger


logger = Logger().logger


class DirectoryAnalyzer:
    def get_md_pathnames(self, pathname: str) -> tp.Iterator[str]:
        logger.debug(f"Init checking {pathname}")
        for (dir_pathname, dirnames, filenames) in os.walk(
            pathname, onerror=self._os_walk_exception_handler
        ):
            # print(dir_pathname, dirnames, filenames)
            for filename in filenames:
                if self._is_md_file(filename):
                    yield str(pathlib.PurePath(dir_pathname, filename))

    def _os_walk_exception_handler(self, exception_instance):
        raise exception_instance

    @staticmethod
    def _is_md_file(filename: str) -> bool:
        return pathlib.PurePath(filename).suffix == ".md"


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
    filename_converted = get_filename_set_extension(filename_to_convert, ".html")
    path_converted_without_analized_path = (
        path_to_convert_without_analized_path.with_name(filename_converted)
    )
    path_converted = pathlib.PurePath(output_directory_pathname).joinpath(
        path_converted_without_analized_path,
    )
    pathname_converted = str(path_converted)
    return pathname_converted


def get_filename_set_extension(filename: str, extension: str) -> str:
    return pathlib.PurePath(filename).with_suffix(extension).name


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


def export_to_file_the_script_combine_files(
    pandoc_metadata_file_pathname: str,
    pandoc_script_convert_md_to_html_file_pathname: str,
    pandoc_template_file_pathname: str,
    md_pathnames_to_convert_file_pathname: str,
    md_pathnames_converted_file_pathname: str,
    css_relative_pathnames_file_pathname: str,
    result_file_pathname: str,
):
    with open(md_pathnames_to_convert_file_pathname) as to_convert_file, open(
        md_pathnames_converted_file_pathname
    ) as converted_file, open(css_relative_pathnames_file_pathname) as css_file, open(
        result_file_pathname, "w"
    ) as script_file:
        to_convert_lines = to_convert_file.read().splitlines()
        converted_lines = converted_file.read().splitlines()
        css_lines = css_file.read().splitlines()
        assert len(to_convert_lines) == len(converted_lines) == len(css_lines)
        for file_to_convert_pathname, file_converted_pathname, css_file_pathname in zip(
            to_convert_lines, converted_lines, css_lines
        ):
            command = "/bin/sh {} {} {} {} {} {}".format(
                pandoc_script_convert_md_to_html_file_pathname,
                file_to_convert_pathname,
                file_converted_pathname,
                css_file_pathname,
                pandoc_template_file_pathname,
                pandoc_metadata_file_pathname,
            )
            logger.debug(f"Command: {command}")
            script_file.write(command)
            script_file.write("\n")


def run(
    css_pathname: str,
    pandoc_metadata_file_pathname: str,
    pandoc_script_convert_md_to_html_file_pathname: str,
    pandoc_template_file_pathname: str,
    pathname_to_analyze: str,
    result_file_pathname: str,
):
    logger.debug(f"Init export file {result_file_pathname}")

    # TODO move constants to config.py
    md_pathnames_to_convert_file_pathname = "/tmp/path-names-to-convert.txt"
    md_pathnames_converted_file_pathname = "/tmp/path-names-converted.txt"
    css_relative_pathnames_file_pathname = "/tmp/css-relative-pathnames.txt"
    export_to_file_the_md_pathnames_to_convert(
        pathname_to_analyze, md_pathnames_to_convert_file_pathname
    )

    export_to_file_the_html_pathnames_converted(
        pathname_to_analyze,
        md_pathnames_to_convert_file_pathname,
        output_directory_pathname="/tmp/cmoli.es/html",
        result_file_pathname=md_pathnames_converted_file_pathname,
    )
    export_to_file_the_css_relative_pathnames(
        css_pathname,
        md_pathnames_to_convert_file_pathname,
        result_file_pathname=css_relative_pathnames_file_pathname,
    )
    export_to_file_the_script_combine_files(
        pandoc_metadata_file_pathname,
        pandoc_script_convert_md_to_html_file_pathname,
        pandoc_template_file_pathname,
        md_pathnames_to_convert_file_pathname,
        md_pathnames_converted_file_pathname,
        css_relative_pathnames_file_pathname,
        f"{result_file_pathname}",
    )


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
