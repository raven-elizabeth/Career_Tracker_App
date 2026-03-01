"""This file defines custom exceptions for the CSV data_access repository.
These exceptions are used to handle specific error cases when working with the CSV file.
Custom exceptions promote more informative error messages and graceful handling of these cases."""


class FileEmptyError(Exception):
    """Raised when the CSV file is found but contains no data.
    Custom exception to distinguish from FileNotFoundError, which is raised when the file does not exist."""
    pass


class DuplicateEntryError(Exception):
    """Raised when attempting to save an entry with a date that already exists in the data_access."""
    pass
