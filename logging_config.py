# Logging is important for tracking the behavior of an application, especially for debugging and monitoring purposes.
# This logging configuration sets up a logger that writes detailed debug information to a file,
# while only showing info and above in the console.

# logger.debug is used for detailed info during dev debugging
# logger.info is used for general info about the application's operation
# logger.warning is used when something unexpected happens but the app can keep running, e.g. invalid requests
# logger.error is used when the app may fail, e.g. file not found, database connection issues, etc.

import logging
import sys
from pathlib import Path

# Path is used to create a logs directory as the parent of this file, where log files will be stored.
LOG_DIR = Path(__file__).parent / "logs"
# mkdir creates the logs directory and exist_ok=True prevents an error if the directory already exists.
LOG_DIR.mkdir(exist_ok=True)


# The method here explicitly returns a logger object, the name is usually set to the name of the module calling it.
def get_logger(name) -> logging.Logger:
    # getLogger retrieves a logger with the specified name. If a logger with that name already exists, it returns the existing logger. If not, it creates a new one.
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Avoid adding duplicate handlers

    logger.setLevel(logging.DEBUG)

    # Define a consistent log format with timestamp, log level, logger name, and message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler: This determines which log messages are printed to the console.
    # Setting it to INFO means that DEBUG messages will not be shown in the console, but will still be logged to the file.
    # StreamHandler is what handles console output, and sys.stdout ensures that logs are printed to standard output.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler: This determines which log messages are written to the log file.
    # Setting it to DEBUG means that all messages will be saved to the file.
    # FileHandler is what handles file output, and we specify the log file path and encoding.
    file_handler = logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
