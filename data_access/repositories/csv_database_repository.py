"""
This class implements the DatabaseRepository interface for a CSV file
data_access (CRUD operations).
Pandas handles the file operations, with to_csv() automatically closing the
file after writing and using mode "a" to append rather than overwrite.
Using Pandas DataFrame simplifies the data manipulation and date indexing
results in O(1) lookups.
"""

from pathlib import Path

import pandas as pd

from data_access.repositories.database_repository import DatabaseRepository
from data_access.repositories.exceptions import (
    DuplicateEntryError,
    FileEmptyError,
)
from domain.dailyentry import DailyEntry
from domain.fields import FIELDS
from logs.logging_config import get_logger


class CsvDatabaseRepository(DatabaseRepository):
    def __init__(self, file_path=None, logger=None):
        super().__init__()
        file_path = (
            file_path if file_path is not None
            else Path(__file__).parents[2] / "data" / "entries.csv"
        )
        self.file_path = Path(file_path)
        self._logger = (
            logger if logger is not None else get_logger(__name__)
        )
        self._logger.debug(
            "CsvDatabaseRepository initialized with file path: %s",
            self.file_path,
        )

        # File is initialised here rather than when writing to the file to
        # ensure it exists before any read operations are attempted, which
        # trigger when the new entry and search screens are created.
        self._initialise_file()

    def _initialise_file(self):
        """Creates the CSV file with headers if it does not exist or is
        completely empty."""
        if (
            not self.file_path.exists()
            or self.file_path.stat().st_size == 0
        ):
            self._logger.info(
                "Initialising CSV file at: %s", self.file_path
            )
            pd.DataFrame(columns=FIELDS).set_index("date").to_csv(
                self.file_path
            )

    def save_entry(self, entry):
        """Saves a new entry to the CSV file.
        Raises DuplicateEntryError if an entry with the same date already
        exists."""
        self._logger.debug(
            "Saving entry with date: %s", entry.entry_dict["date"]
        )
        data = entry.entry_dict
        df = pd.DataFrame([data])
        df = self._set_date_index(df)

        file_size = self.file_path.stat().st_size
        file_empty = file_size == 0

        # Check for duplicate entry by date before saving
        if not file_empty:
            entry_date = str(entry.entry_dict["date"])
            if self._entry_exists(entry_date):
                self._logger.warning(
                    "Attempted to save duplicate entry with date: %s",
                    entry.entry_dict["date"],
                )
                raise DuplicateEntryError(
                    f"An entry with date {entry.entry_dict['date']} "
                    f"already exists."
                )

        # Only write the header if the file is empty (i.e. no entries have
        # been saved yet)
        header = file_empty
        df.to_csv(self.file_path, mode="a", header=header, lineterminator="\n")
        self._logger.info(
            "Entry saved successfully for date: %s",
            entry.entry_dict["date"],
        )

    def _entry_exists(self, date):
        """Helper method to check if an entry with the given date already
        exists in the CSV file."""
        existing_df = pd.read_csv(
            self.file_path, index_col="date", dtype=str, na_filter=False
        )
        exists = date in existing_df.index
        self._logger.debug(
            "Checked for existing entry with date: %s. Exists: %s",
            date,
            exists,
        )
        return exists

    @staticmethod
    def _set_date_index(df):
        """Set the 'date' column as the DataFrame index.

        Converts to datetime first to normalise any date format variations,
        then immediately converts back to a date string to prevent pandas
        from appending time data (e.g. '2025-01-01 00:00:00').
        """
        df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
        df = df.set_index("date")
        return df

    def get_entry_by_date(self, date):
        """Retrieve an entry by its date. Returns None if no entry is found.
        Does not raise for a missing entry — this is intentional, as the
        method is called during date selection in the GUI where no entry is
        a valid state. Raises FileNotFoundError or FileEmptyError if the
        file is unavailable."""
        self._logger.debug("Searching for entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(
            self.file_path, index_col="date", dtype=str, na_filter=False
        )

        if date in df.index:
            self._logger.debug("Entry found for date: %s", date)
            # Locate the row by date index and convert to dictionary, then
            # create an Entry object through unpacking
            entry_data = df.loc[date].to_dict()
            # Ensure the date is included in the entry data
            entry_data["date"] = date
            # Stored data is generally trusted, but as a user could edit the
            # CSV file manually, we should still validate that the entry
            # contains at least one non-empty value (besides date) before
            # creating the Entry object
            return DailyEntry.from_create_entry_request(entry_data)

        self._logger.warning("No entry found for date: %s", date)
        return None

    def replace_entry(self, date, updated_entry):
        """Replaces an existing entry with the given date.
        Raises ValueError if no entry is found for the given date."""
        self._logger.debug("Replacing entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(
            self.file_path, index_col="date", dtype=str, na_filter=False
        )

        if date in df.index:
            updated_data = updated_entry.entry_dict

            for field, value in updated_data.items():
                if field != "date":
                    df.at[date, field] = value

            df.to_csv(self.file_path)
            self._logger.info(
                "Entry replaced successfully for date: %s", date
            )
        else:
            self._logger.warning(
                "No entry found to replace for date: %s", date
            )
            raise ValueError(f"No entry found for date: {date}")

    @staticmethod
    def _get_merged_entry(update_request, df):
        """Merge patch fields into the existing row, skipping any keys not
        in df.columns (e.g. date)."""
        date = update_request["date"]
        existing = df.loc[date].to_dict()
        return {
            field: (
                update_request[field]
                if field in update_request
                else value
            )
            for field, value in existing.items()
            if field in df.columns
        }

    def partially_update_entry(self, update_request):
        """Partially updates an existing entry with the given date and fields
        to update. Raises ValueError if no entry is found for the given
        date."""
        date = update_request["date"]
        self._logger.debug(
            "Partially updating entry with date: %s", date
        )
        self._validate_file()
        df = pd.read_csv(
            self.file_path, index_col="date", dtype=str, na_filter=False
        )

        if date in df.index:
            merged_entry = self._get_merged_entry(update_request, df)

            # Guard: reject the patch if the merged result would leave all
            # fields empty
            if not any(merged_entry.values()):
                self._logger.warning(
                    "PATCH for date %s rejected: merged result would have"
                    " no non-empty fields",
                    date,
                )
                raise ValueError(
                    "Patch would result in an empty entry: at least one "
                    "field must remain non-empty"
                )

            # Write only the changed fields — merged_entry keys are already
            # valid columns (date excluded)
            for field, value in merged_entry.items():
                if field in update_request:
                    df.at[date, field] = value
            df.to_csv(self.file_path)
            self._logger.info(
                "Entry partially updated successfully for date: %s", date
            )
            return self.get_entry_by_date(date)

        else:
            self._logger.warning(
                "No entry found to partially update for date: %s", date
            )
            raise ValueError(f"No entry found for date: {date}")

    def delete_entry(self, date):
        """Deletes an entry by its date.
        Raises ValueError if no entry is found for the given date."""
        self._logger.debug("Deleting entry with date: %s", date)
        self._validate_file()
        df = pd.read_csv(
            self.file_path, index_col="date", dtype=str, na_filter=False
        )

        if date in df.index:
            df = df.drop(date)
            df.to_csv(self.file_path)
            self._logger.info(
                "Entry deleted successfully for date: %s", date
            )
        else:
            self._logger.warning(
                "No entry found to delete for date: %s", date
            )
            raise ValueError(f"No entry found for date: {date}")

    def _validate_file(self):
        """Helper method to validate the existence and non-emptiness of the
        CSV file before performing read/write operations."""
        if not self.file_path.exists():
            self._logger.error("File not found: %s", self.file_path)
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )
        elif self.file_path.stat().st_size == 0:
            self._logger.error(
                "No data found in file: %s", self.file_path
            )
            raise FileEmptyError(
                f"No data found in file: {self.file_path}"
            )

