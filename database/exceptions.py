# Created custom exception for empty file as using FileNotFoundError would be a misleading title
class FileEmptyError(Exception):
    pass


class DuplicateEntryError(Exception):
    pass
