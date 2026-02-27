# Created custom exception for empty file as using FileNotFoundError would be a misleading title
class FileEmptyError(Exception):
    """Raised when the CSV file is found but contains no data."""
    pass


class DuplicateEntryError(Exception):
    """Raised when attempting to save an entry with a date that already exists in the database."""
    pass
