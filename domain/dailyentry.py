"""
Defines the DailyEntry domain model.

The entry dictionary is created dynamically based on FIELDS, which are stored in a
separate file to support the open/closed principle.
kwargs.get() defaults missing keys to None (or empty string if specified) rather than raising KeyError.
"""

from domain.fields import FIELDS


class DailyEntry:
    def __init__(self, **kwargs):
        if not kwargs.get("date"):
            raise ValueError("Unable to create entry: No date provided")

        self.entry_dict = {field: kwargs.get(field, "") for field in FIELDS}
        for k, v in self.entry_dict.items():
            if v is None:
                self.entry_dict[k] = ""

        if not any(self.entry_dict[field] for field in FIELDS if field != "date"):
            raise ValueError("Unable to create entry: At least one value must not be empty")

    @classmethod
    def from_replace_request(cls, update_dict):
        """Validate that all fields are present for a full replacement (PUT), then construct the entry."""
        if not update_dict or not all(field in update_dict for field in FIELDS):
            raise ValueError("PUT request requires replacement data for all fields in the Entry class")
        return cls(**update_dict)

    @classmethod
    def from_partial_update_request(cls, update_dict):
        """Validate that at least one non-empty value is provided for a partial update (PATCH),
        then construct the entry."""
        if all(values.strip() == "" for values in update_dict.values()):
            raise ValueError("PATCH request requires at least one non-empty value for update")
        return cls(**update_dict)
