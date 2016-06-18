import logging
from datetime import datetime
from os import path, makedirs
from config import Configuration
from singletonmixin import Singleton

DEFAULT_LOGFOLDER = path.join(path.expanduser('~'), "app", "log")

class Logger(Singleton):

    def __init__(self, log_folder=None, file_name="stock_tracer_{0}.log"):
        logger = logging.getLogger('stock_tracer')
        logger.setLevel(logging.DEBUG)

        # create file log
        log_folder = log_folder if log_folder else DEFAULT_LOGFOLDER
        if not path.exists(log_folder):
            makedirs(log_folder)

        log_file_name = file_name.format(datetime.now().strftime("%Y-%m-%d"))
        fh = logging.FileHandler(path.join(log_folder, log_file_name))
        fh.setLevel(logging.DEBUG)

        # create console log
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

    def get(self, logger_name):
        """get logging instance

        :param logger_name:
        """
        if "stock_tracer" not in logger_name:
            logger_name = "stock_tracer." + logger_name

        logger = logging.getLogger(logger_name)
        logger.disabled = False
        return logger

Logger = Logger.getInstance(Configuration.get("log_folder"))
