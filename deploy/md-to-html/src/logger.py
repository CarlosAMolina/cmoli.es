import logging
import pathlib
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
