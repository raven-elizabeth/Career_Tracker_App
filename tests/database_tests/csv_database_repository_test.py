# This file contains unit tests for the CsvDatabaseRepository class.
# The tests use the AAA (Arrange, Act, Assert) pattern to structure the test cases.

import csv
import tempfile
import os
import unittest
from domain.entry import Entry
from database.csv_database_repository import CsvDatabaseRepository


class TestCsvDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self._testDir = tempfile.TemporaryDirectory()
        self._test_file_path = os.path.join(self._testDir.name, "test_entries.csv")
        self._repo = CsvDatabaseRepository(file_path=self._test_file_path)

        self.entry = Entry(
            date="2025-06-04",
            work_contribution="Completed unit tests for whole codebase",
            learning="Discovered how to use setUp and tearDown in unittest"
        )
        self.expected = {
            "date": "2025-06-04",
            "work_contribution": "Completed unit tests for whole codebase",
            "learning": "Discovered how to use setUp and tearDown in unittest",
            "win": "",
            "challenge": "",
            "next_steps": ""
        }

        self._repo.save_entry(self.entry)

    def tearDown(self):
        self._testDir.cleanup()

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

    def test_saving_existing_entry_raises_value_error(self):
        # Arrange
        duplicate_entry = Entry(
            date="2025-06-04",
            work_contribution="Attempting to save duplicate entry"
        )

        # Act
        with self.assertRaises(ValueError) as context:
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
        second_entry = Entry(**second_value)
        self._repo.save_entry(second_entry)

        # Act
        response = self._repo.get_entry_by_date("2025-06-05")

        # Assert
        self.assertEqual(response.entry_dict, second_value)

    def test_value_error_raised_when_get_date_not_found(self):
        # Arrange
        with self.assertRaises(ValueError) as context:
            # Act
            self._repo.get_entry_by_date("2025-06-06")

        # Assert
        self.assertEqual(str(context.exception), "No entry found for date: 2025-06-06")

    def test_update_entry_updates_existing_entry(self):
        # Arrange
        updated_entry = Entry(
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

        self._repo.update_entry("2025-06-04", updated_entry)
        response = self._repo.get_entry_by_date("2025-06-04")
        self.assertEqual(response.entry_dict, updated_entry.entry_dict)

    def test_update_nonexistent_entry_raises_value_error(self):
        # Arrange
        updated_entry = Entry(
            date="2025-06-07",
            work_contribution="Updated work contribution",
            learning="Updated learning",
            win="Added win",
            challenge="Added challenge",
            next_steps="Added next steps"
        )

        # Act, Assert
        with self.assertRaises(ValueError) as context:
            self._repo.update_entry("2025-06-07", updated_entry)

        self.assertEqual(str(context.exception), "No entry found for date: 2025-06-07")

    def test_delete_existing_entry_deletes_entry(self):
        pass