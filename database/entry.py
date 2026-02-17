class Entry:
    def __init__(self, **kwargs):
        if not kwargs.get("date"):
            raise ValueError("Unable to create entry: No date provided")

        self.fields = ["date", "work_contribution", "learning", "win", "challenge", "next_steps"]
        self.entry_dict = {field: kwargs.get(field) for field in self.fields}

        if not any(self.entry_dict[field] for field in self.fields if field != "date"):
            raise ValueError("Unable to create entry: At least one value must not be empty")