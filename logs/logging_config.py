"""
Logging is important for tracking the behavior of an application, especially
for debugging and monitoring purposes.
This logging configuration sets up a logger that writes detailed debug
information to a file, while only showing info and above in the console.

logger.debug is used for detailed info during dev debugging
logger.info is used for general info about the application's operation
logger.warning is used when something unexpected happens but the app can
  keep running, e.g. invalid requests
logger.error is used when the app may fail, e.g. file not found,
  data_access connection issues, etc.
"""

import logging
import sys
from pathlib import Path

# Path(__file__).parent resolves to the logs/ directory where this file
# lives — log files are stored here.
LOG_DIR = Path(__file__).parent
LOG_DIR.mkdir(exist_ok=True)  # Ensure the log directory exists


def get_logger(name) -> logging.Logger:
    """Set up and return a logger with the specified name, configured to log
    to both console and file with appropriate levels and formatting.
    The method explicitly returns a logger object; the name is usually the
    module calling it."""
    # getLogger retrieves a logger with the given name, or creates one if it
    # does not exist.
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Avoid adding duplicate handlers

    logger.setLevel(logging.DEBUG)

    # Define a consistent log format with timestamp, log level, logger name,
    # and message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler: determines which log messages are printed to the
    # console. Setting it to INFO means DEBUG messages will not be shown in
    # the console, but will still be logged to file.
    # StreamHandler handles console output; sys.stdout ensures logs are
    # printed to standard output.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler: determines which log messages are written to the log
    # file. Setting it to DEBUG means all messages will be saved to file.
    # FileHandler handles file output; we specify the log file path and
    # encoding.
    file_handler = logging.FileHandler(
        LOG_DIR / "app.log", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
