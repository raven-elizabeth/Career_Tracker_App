"""
Defines the DailyEntry domain model.

The entry dictionary is created dynamically based on FIELDS, which are stored in a
separate file to support the open/closed principle.
kwargs.get() defaults missing keys to None (or empty string if specified) rather than raising KeyError.
"""

from domain.fields import FIELDS


class DailyEntry:
    def __init__(self, **kwargs):
        """Initializes the DailyEntry with a dictionary of field values based on FIELDS."""
        # Validate that a date is provided, since it's required for all operations
        # and serves as the unique identifier for entries.
        if not kwargs.get("date"):
            raise ValueError("Unable to create entry: No date provided")

        # Create the entry dictionary by extracting values for each field from kwargs,
        # defaulting to empty string if not provided.
        self.entry_dict = {field: kwargs.get(field, "") for field in FIELDS}
        for k, v in self.entry_dict.items():
            # Extra guard against None values
            if v is None:
                self.entry_dict[k] = ""

    @staticmethod
    def _validate_non_empty(entry_dict):
        """Helper to validate that at least one non-date field has a non-empty value."""
        if not any(entry_dict.get(field, "") for field in FIELDS if field != "date"):
            raise ValueError("Unable to create entry: At least one value must not be empty")

    @classmethod
    def from_replace_request(cls, update_dict):
        """Validate that all fields are present & at least one value non-empty for a full replacement (PUT),
        then construct the entry."""
        if not update_dict or not all(field in update_dict for field in FIELDS):
            raise ValueError("PUT request requires replacement data for all fields in the Entry class")
        cls._validate_non_empty(update_dict)
        return cls(**update_dict)

    @classmethod
    def from_create_entry_request(cls, entry_dict):
        """Validate that entry contains at least one non-empty value (besides date), then construct the entry."""
        cls._validate_non_empty(entry_dict)
        return cls(**entry_dict)

    @classmethod
    def from_partial_update_request(cls, update_dict):
        """Construct an entry from a partial update (PATCH) without validating non-empty fields,
        since the patch may be intended to clear out values.
        Could just call the constructor directly, but this method is provided for consistency
        and explicitness as the other routes have their own class methods."""
        return cls(**update_dict)
