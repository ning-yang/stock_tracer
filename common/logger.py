import logging
from datetime import datetime
from os import path, makedirs
from config import Configuration
from singletonmixin import Singleton

DEFAULT_LOGFOLDER = path.join(path.expanduser('~'), "app", "log")

class Logger(Singleton):
    """Logger"""

    def __init__(self):
        """__init__"""
        self.is_initialized = False

    def setup(self, log_folder=None, file_name="stock_tracer_{0}.log"):
        """setup

        :param log_folder:
        :param file_name:
        """
        log_config = Configuration.get("logging")

        logger = logging.getLogger('stock_tracer')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')

        # create file log
        if log_config["file"]:
            log_folder = log_folder if log_folder else DEFAULT_LOGFOLDER
            if not path.exists(log_folder):
                makedirs(log_folder)

            log_file_name = file_name.format(datetime.now().strftime("%Y-%m-%d"))
            fh = logging.FileHandler(path.join(log_folder, log_file_name))
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        # create console log
        if log_config["console"]:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        self.is_initialized = True

    def get(self, logger_name):
        """get logging instance

        :param logger_name:
        """
        if not self.is_initialized:
            self.setup(Configuration.get("log_folder"))

        if "stock_tracer" not in logger_name:
            logger_name = "stock_tracer." + logger_name

        logger = logging.getLogger(logger_name)
        logger.disabled = False
        return logger

Logger = Logger.getInstance()
