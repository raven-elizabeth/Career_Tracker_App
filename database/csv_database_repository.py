# This class implements the DatabaseRepository interface for a CSV file database (CRUD operations).
# Pandas handles the file operations, with to_csv() automatically closing the file after writing and using mode "a" to append rather than overwrite.
# Using Pandas DataFrame simplifies the data manipulation.

from database.database_repository import DatabaseRepository
import pandas as pd
from pathlib import Path
from domain.entry import Entry


class CsvDatabaseRepository(DatabaseRepository):
    def __init__(self, file_path="entries.csv"):
        super().__init__()
        self.file_path = Path(file_path)

    def save_entry(self, entry):
        data = entry.entry_dict
        df = pd.DataFrame([data])

        # Copilot suggested converting to datetime to ensure correct formatting and then saving as string prevents pandas adding time data
        df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
        df = df.set_index("date").sort_index()

        header = not self.file_path.exists() or self.file_path.stat().st_size == 0
        df.to_csv(self.file_path, mode="a", header=header)

    def get_entry_by_date(self, date):
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            raise ValueError(f"No entry found for date: {date}")

        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        date_value = str(date)
        if date_value in df.index:
            # Locate the row by date index and convert to dictionary, then create an Entry object through unpacking
            entry_data = df.loc[date_value].to_dict()
            entry_data['date'] = date_value
            return Entry(**entry_data)

    def update_entry(self, entry_id, updated_entry):
        pass

    def delete_entry(self, entry_id):
        pass

        # # Read the CSV using string dtypes so empty fields remain empty strings (not NaN)
        # df = pd.read_csv(self.file_path, index_col="date", dtype=str)
        #
        # # Ensure index values are strings so the passed entry_date (string) can be matched
        # df.index = df.index.astype(str)
        #
        # if str(entry_date) in df.index:
        #     entry_data = df.loc[str(entry_date)].to_dict()
