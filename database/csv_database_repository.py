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
        df = self.set_date_index(df)

        file_exists = self.file_path.exists()
        file_size = self.file_path.stat().st_size if file_exists else 0

        # Check for duplicate entry by date before saving
        if file_exists and file_size > 0:
            if self.entry_exists(str(entry.entry_dict["date"])):
                raise ValueError(f"An entry with date {entry.entry_dict['date']} already exists.")

        # Check if the file exists and is not empty to determine whether to write the header (only write if writing first entry)
        header = not file_exists or file_size == 0
        df.to_csv(self.file_path, mode="a", header=header)

    def entry_exists(self, date):
        existing_df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)
        return True if date in existing_df.index else False

    @staticmethod
    def set_date_index(df):
        # Copilot suggested converting to datetime to ensure correct formatting and then saving as string prevents pandas adding time data
        df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
        df = df.set_index("date")
        return df

    def get_entry_by_date(self, date):
        self.validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        date_value = str(date)
        if date_value in df.index:
            # Locate the row by date index and convert to dictionary, then create an Entry object through unpacking
            entry_data = df.loc[date_value].to_dict()
            entry_data['date'] = date_value
            return Entry(**entry_data)
        raise ValueError(f"No entry found for date: {date}")

    def update_entry(self, date, updated_entry):
        self.validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        if date in df.index:
            updated_data = updated_entry.entry_dict
            for field in updated_data:
                df.at[date, field] = updated_data[field]
            df.to_csv(self.file_path)
        else:
            raise ValueError(f"No entry found for date: {date}")

    def delete_entry(self, date):
        self.validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        if date in df.index:
            df = df.drop(date)
            df.to_csv(self.file_path)
        else:
            raise ValueError(f"No entry found for date: {date}")

    def validate_file(self):
        if not self.file_path.exists():
            raise ValueError(f"File not found: {self.file_path}")
        elif self.file_path.stat().st_size == 0:
            raise ValueError(f"No data found in file: {self.file_path}")