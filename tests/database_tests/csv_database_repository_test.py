# This file contains unit tests for the CsvDatabaseRepository class.
# The tests use the AAA (Arrange, Act, Assert) pattern to structure the test cases.

import csv
import os
import tempfile
import unittest

from database.csv_database_repository import CsvDatabaseRepository
from database.exceptions import FileEmptyError, DuplicateEntryError
from domain.dailyentry import DailyEntry


class TestCsvDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self._test_dir = tempfile.TemporaryDirectory()
        self._test_file_path = os.path.join(self._test_dir.name, "test_entries.csv")
        self._repo = CsvDatabaseRepository(file_path=self._test_file_path)

        self.entry = DailyEntry(
            date="2025-06-04",
            work_contribution="Completed unit tests for whole codebase",
            learning="Discovered how to use setUp and tearDown in unittest",
            win="Refactored code to be cleaner"
        )
        self.expected = {
            "date": "2025-06-04",
            "work_contribution": "Completed unit tests for whole codebase",
            "learning": "Discovered how to use setUp and tearDown in unittest",
            "win": "Refactored code to be cleaner",
            "challenge": "",
            "next_steps": ""
        }

        self._repo.save_entry(self.entry)

    def tearDown(self):
        self._test_dir.cleanup()

    def test_save_partial_entry_saves_all_fields_with_defaults(self):
        # Assert
        with open(self._repo.file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 1)

            # The code below was modified with the help of GitHub Copilot; The assertion accepts both the "YYYY-MM-DD" or "YYYY-MM-DD 00:00:00" format that may be returned from pandas
            self.assertTrue(rows[0]['date'].startswith(self.expected['date']))
            # The original suggestion for the line below was unnecessarily complex, comparing each field separately
            self.assertEqual(self.expected, rows[0])

    def test_saving_existing_entry_raises_duplicate_error(self):
        # Arrange
        duplicate_entry = DailyEntry(
            date="2025-06-04",
            work_contribution="Attempting to save duplicate entry"
        )

        # Act
        with self.assertRaises(DuplicateEntryError) as context:
            self._repo.save_entry(duplicate_entry)

        # Assert
        self.assertEqual(str(context.exception), "An entry with date 2025-06-04 already exists.")

    def test_get_existing_entry_by_date_returns_entry(self):
        # Arrange
        second_value = {
            "date": "2025-06-05",
            "work_contribution": "Completed unit tests for get_entries method",
            "learning": "Discovered how to use temp file",
            "win": "Successfully retrieved entry by date",
            "challenge": "Had to learn how to use temp file module for testing",
            "next_steps": "Continue adding more tests and refactor code as needed"
        }
        second_entry = DailyEntry(**second_value)
        self._repo.save_entry(second_entry)

        # Act
        response = self._repo.get_entry_by_date("2025-06-05")

        # Assert
        self.assertEqual(response.entry_dict, second_value)

    def test_none_returned_when_get_date_not_found(self):
        # Act
        entry = self._repo.get_entry_by_date("2025-06-06")

        # Assert
        self.assertIsNone(entry)

    def test_replace_entry_updates_existing_entry(self):
        # Arrange
        updated_entry = DailyEntry(
            date="2025-06-04",
            work_contribution="Updated work contribution",
            learning="Updated learning",
            win="Added win",
            challenge="Added challenge",
            next_steps="Added next steps"
        )

        # Act, Assert
        response = self._repo.get_entry_by_date("2025-06-04")
        self.assertEqual(response.entry_dict, self.expected)

        self._repo.replace_entry("2025-06-04", updated_entry)
        response = self._repo.get_entry_by_date("2025-06-04")
        self.assertEqual(response.entry_dict, updated_entry.entry_dict)

    def test_replace_nonexistent_entry_raises_value_error(self):
        # Arrange
        updated_entry = DailyEntry(
            date="2025-06-07",
            work_contribution="Updated work contribution",
            learning="Updated learning",
            win="Added win",
            challenge="Added challenge",
            next_steps="Added next steps"
        )

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            self._repo.replace_entry("2025-06-07", updated_entry)

        self.assertEqual(str(context.exception), "No entry found for date: 2025-06-07")

    def test_partially_update_entry_updates_only_provided_fields(self):
        # Arrange
        updated_entry_items = {
            "date": "2025-06-04",
            "work_contribution": "Partially update for work contribution"
        }

        expected_entry = {
            "date": "2025-06-04",
            "work_contribution": "Partially update for work contribution",
            "learning": "Discovered how to use setUp and tearDown in unittest",
            "win": "Refactored code to be cleaner",
            "challenge": "",
            "next_steps": ""
        }

        # Act
        self._repo.partially_update_entry(updated_entry_items)
        response = self._repo.get_entry_by_date("2025-06-04")

        # Assert
        self.assertEqual(response.entry_dict, expected_entry)

    def test_partially_update_nonexistent_entry_raises_value_error(self):
        # Arrange
        updated_entry = DailyEntry(
            date="2025-06-07",
            work_contribution="Partially update for work contribution"
        )

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            self._repo.partially_update_entry(updated_entry.entry_dict)

        self.assertEqual(str(context.exception), "No entry found for date: 2025-06-07")

    def test_delete_existing_entry_deletes_entry(self):
        # Arrange
        get_response = self._repo.get_entry_by_date("2025-06-04")
        self.assertEqual(get_response.entry_dict, self.expected)

        # Act
        self._repo.delete_entry("2025-06-04")
        deleted_entry_get_response = self._repo.get_entry_by_date("2025-06-04")

        # Assert
        self.assertIsNone(deleted_entry_get_response)

    def test_delete_nonexistent_entry_raises_value_error(self):
        # Arrange
        with self.assertRaises(ValueError) as context:
            # Act
            self._repo.delete_entry("2025-06-08")

        # Assert
        self.assertEqual(str(context.exception), "No entry found for date: 2025-06-08")

    def test_validate_file_raises_file_not_found_error_if_file_does_not_exist(self):
        # Arrange
        test_repo = CsvDatabaseRepository(file_path="non_existent_file.csv")

        # Act
        with self.assertRaises(FileNotFoundError) as context:
            # Assert
            test_repo._validate_file()

        self.assertEqual(str(context.exception), f"File not found: {test_repo.file_path}")

    def test_validate_file_raises_file_empty_error_if_file_is_empty(self):
        # Arrange
        with open(self._test_file_path, 'w') as file:
            file.close()

        test_repo = CsvDatabaseRepository(self._test_file_path)

        # Act
        with self.assertRaises(FileEmptyError) as context:
            # Assert
            test_repo._validate_file()

        self.assertEqual(str(context.exception), f"No data found in file: {test_repo.file_path}")
