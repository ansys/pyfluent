import logging
import os
import tempfile
from pathlib import Path


class Logger:
    def __init__(self, level=logging.ERROR):
        self.logger = logging.getLogger()
        self.stream_handler = None
        self.file_handler = None
        self.log_filepath = None
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        self.enable_logging_to_stdout()
        self.logger.setLevel(level)

        # Writing logging methods.
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.log = self.logger.log

    def set_level(self, level):
        self.logger.setLevel(level)

    def get_default_log_filepath(self):
        fd, filepath = tempfile.mkstemp(
            suffix=f"-{os.getpid()}.txt",
            prefix="pyfluent-",
            dir=str(Path.cwd()),
        )
        os.close(fd)
        return Path(filepath)

    def enable_logging_to_stdout(self):
        if self.stream_handler is None:
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def disable_logging_to_stdout(self):
        self.logger.removeHandler(self.stream_handler)

    def enable_logging_to_file(self, filepath=None):
        self.logger.removeHandler(self.file_handler)
        if not filepath and not self.log_filepath:
            self.log_filepath = self.get_default_log_filepath()
        elif filepath:
            self.log_filepath = Path(filepath)
        self.file_handler = logging.FileHandler(self.log_filepath)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def disable_logging_to_file(self):
        self.logger.removeHandler(self.file_handler)
