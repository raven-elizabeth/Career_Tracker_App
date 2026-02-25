# The Entry class represents a single entry in the database. It requires a date and at least one of the other fields to be not empty.
# The fields are stored in a separate file to make the code open for extension (open/closed principle)
# The entry dictionary is  created dynamically based on the fields.
# .get() is used to retrieve values from kwargs because it defaults to None values if the key does not exist

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
        if not update_dict or not all(field in update_dict for field in FIELDS):
            raise ValueError("PUT request requires replacement data for all fields in the Entry class")
        return cls(**update_dict)

    @classmethod
    def from_partial_update_request(cls, update_dict):
        if all(values.strip() == "" for values in update_dict.values()):
            raise ValueError("PATCH request requires at least one non-empty value for update")
        return cls(**update_dict)