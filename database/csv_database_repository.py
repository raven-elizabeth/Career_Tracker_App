# This class implements the DatabaseRepository interface for a CSV file database (CRUD operations).
# Pandas handles the file operations, with to_csv() automatically closing the file after writing and using mode "a" to append rather than overwrite.
# Using Pandas DataFrame simplifies the data manipulation.

from database.database_repository import DatabaseRepository
import pandas as pd
from pathlib import Path


class CsvDatabaseRepository(DatabaseRepository):
    def __init__(self, file_path="entries.csv"):
        super().__init__()
        self.file_path = Path(file_path)

    def save_entry(self, entry):
        data = entry.entry_dict
        df = pd.DataFrame([data])

        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date").sort_index()
        df.index.name = "date"

        header = not self.file_path.exists() or self.file_path.stat().st_size == 0
        df.to_csv(self.file_path, mode="a", header=header)

    def get_entries(self):
        with open(self.file_path, 'r') as file:
            pass

    def get_entry_by_date(self, entry_date):
       with open(self.file_path, 'r') as file:
            pass

    def update_entry(self, entry_id, updated_entry):
        with open(self.file_path, 'r+') as file:
            pass

    def delete_entry(self, entry_id):
        with open(self.file_path, 'r+') as file:
            pass