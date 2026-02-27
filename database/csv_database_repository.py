# This class implements the DatabaseRepository interface for a CSV file database (CRUD operations).
# Pandas handles the file operations, with to_csv() automatically closing the file after writing
# and using mode "a" to append rather than overwrite.
# Using Pandas DataFrame simplifies the data manipulation and date indexing results in O(1) lookups

from pathlib import Path

import pandas as pd

from database.database_repository import DatabaseRepository
from database.exceptions import FileEmptyError, DuplicateEntryError
from domain.dailyentry import DailyEntry
from logging_config import get_logger


class CsvDatabaseRepository(DatabaseRepository):
    def __init__(self, file_path=None, logger=None):
        super().__init__()
        file_path = file_path if not None else Path(__file__).parent / "entries.csv"
        self.file_path = Path(file_path)
        self._logger = logger if logger else get_logger(__name__)
        self._logger.debug("CsvDatabaseRepository initialized with file path: %s", self.file_path)

    def save_entry(self, entry):
        """Saves a new entry to the CSV file. Raises DuplicateEntryError if an entry with the same date already exists."""

        self._logger.debug("Saving entry with date: %s", entry.entry_dict["date"])
        data = entry.entry_dict
        df = pd.DataFrame([data])
        df = self._set_date_index(df)

        file_exists = self.file_path.exists()
        file_size = self.file_path.stat().st_size if file_exists else 0

        # Check for duplicate entry by date before saving
        if file_exists and file_size > 0:
            entry_date = str(entry.entry_dict["date"])
            if self._entry_exists(entry_date):
                self._logger.warning(
                    "Attempted to save duplicate entry with date: %s",
                    entry.entry_dict["date"]
                )
                raise DuplicateEntryError(f"An entry with date {entry.entry_dict['date']} already exists.")

        # Check if the file exists and is not empty to determine whether to write the header
        # (only write if writing first entry)
        header = not file_exists or file_size == 0
        df.to_csv(self.file_path, mode="a", header=header)
        self._logger.info("Entry saved successfully for date: %s", entry.entry_dict["date"])

    def _entry_exists(self, date):
        """Helper method to check if an entry with the given date already exists in the CSV file."""

        existing_df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)
        exists = date in existing_df.index
        self._logger.debug("Checked for existing entry with date: %s. Exists: %s", date, exists)
        return exists

    @staticmethod
    def _set_date_index(df):
        """Helper method to set the 'date' column as the index of the DataFrame, ensuring correct formatting."""

        # Copilot suggested converting to datetime to ensure correct formatting
        # Then saving as string prevents pandas adding time data
        df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
        df = df.set_index("date")
        return df

    def get_entry_by_date(self, date):
        """Retrieves an entry by its date. Returns None if no entry is found for the given date.
        Does not raise an error for missing entry
        - this is by design as this method is used during date selection on the GUI"""

        self._logger.debug("Searching for entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        if date in df.index:
            self._logger.debug("Entry found for date: %s", date)
            # Locate the row by date index and convert to dictionary, then create an Entry object through unpacking
            entry_data = df.loc[date].to_dict()
            # Ensure the date is included in the entry data
            entry_data["date"] = date
            return DailyEntry(**entry_data)

        self._logger.warning("No entry found for date: %s", date)
        return None

    def replace_entry(self, date, updated_entry):
        """Replaces an existing entry with the given date. Raises ValueError if no entry is found for the given date."""

        self._logger.debug("Replacing entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        if date in df.index:
            updated_data = updated_entry.entry_dict

            for field, value in updated_data.items():
                if field != "date":
                    df.at[date, field] = value

            df.to_csv(self.file_path)
            self._logger.info("Entry replaced successfully for date: %s", date)
        else:
            self._logger.warning("No entry found to replace for date: %s", date)
            raise ValueError(f"No entry found for date: {date}")

    def partially_update_entry(self, update_request):
        """Partially updates an existing entry with the given date and fields to update.
        Raises ValueError if no entry is found for the given date."""

        date = update_request["date"]
        self._logger.debug("Partially updating entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        if date in df.index:
            for field, value in update_request.items():
                if field in df.columns:
                    df.at[date, field] = value
                else:
                    self._logger.debug(
                        "Field '%s' not found in existing entry for date: %s. Skipping update for this field.",
                        field,
                        date
                    )
            df.to_csv(self.file_path)
            self._logger.info("Entry partially updated successfully for date: %s", date)
            return self.get_entry_by_date(date)

        else:
            self._logger.warning("No entry found to partially update for date: %s", date)
            raise ValueError(f"No entry found for date: {date}")

    def delete_entry(self, date):
        """Deletes an entry by its date. Raises ValueError if no entry is found for the given date."""

        self._logger.debug("Deleting entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(self.file_path, index_col="date", dtype=str, na_filter=False)

        if date in df.index:
            df = df.drop(date)
            df.to_csv(self.file_path)
            self._logger.info("Entry deleted successfully for date: %s", date)
        else:
            self._logger.warning("No entry found to delete for date: %s", date)
            raise ValueError(f"No entry found for date: {date}")

    def _validate_file(self):
        """Helper method to validate the existence and non-emptiness of the CSV file
        before performing read/write operations."""

        if not self.file_path.exists():
            self._logger.error("File not found: %s", self.file_path)
            raise FileNotFoundError(f"File not found: {self.file_path}")
        elif self.file_path.stat().st_size == 0:
            self._logger.error("No data found in file: %s", self.file_path)
            raise FileEmptyError(f"No data found in file: {self.file_path}")
