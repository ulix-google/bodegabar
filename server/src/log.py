import logging
import sys

LOG_FILENAME = "bodegabar.log"
LOG_FORMAT = "%(levelname)s: %(asctime)s %(message)s"

def configure_logging():
    """Configures logging.

    Configured logging for the application with 2 distinct handlers: one for
    printing to stdout, and another for logging to a file. Both logging handlers
    have a format of: `%(levelname)s: %(asctime)s %(message)s`. The log file
    is created at the same directory level as `main.py`.

    Args:
        None

    Returns:
        None
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(_configure_file_logging_handler())
    root.addHandler(_configure_stream_logging_handler())

def _configure_stream_logging_handler() -> logging.StreamHandler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    return handler

def _configure_file_logging_handler() -> logging.FileHandler:
    handler = logging.FileHandler(filename=LOG_FILENAME)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    return handler