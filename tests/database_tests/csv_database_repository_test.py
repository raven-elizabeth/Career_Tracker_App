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

    def tearDown(self):
        self._testDir.cleanup()

    def test_save_entry(self):
        # Act
        self._repo.save_entry(self.entry)

        # Assert
        with open(self._repo.file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 1)

            # The code below was modified with the help of GitHub Copilot; The assertion accepts both the "YYYY-MM-DD" or "YYYY-MM-DD 00:00:00" format that may be returned from pandas
            self.assertTrue(rows[0]['date'].startswith(self.expected['date']))
            # The original suggestion for the line below was unnecessarily complex, comparing each field separately
            self.assertEqual(self.expected, rows[0])

    def test_get_entry_by_date(self):
        # Arrange
        self._repo.save_entry(self.entry)
        second_value = {
            "date": "2025-06-05",
            "work_contribution": "Completed unit tests for get_entries method",
            "learning": "Discovered how to use temp file",
            "win": "",
            "challenge": "",
            "next_steps": ""
        }
        second_entry = Entry(**second_value)
        self._repo.save_entry(second_entry)

        # Act
        result = self._repo.get_entry_by_date("2025-06-05")

        # Assert
        self.assertEqual(result.entry_dict, second_value)

    def test_get_entry_by_date_not_found(self):
        with self.assertRaises(ValueError) as context:
            self._repo.get_entry_by_date("2025-06-06")

        self.assertEqual(str(context.exception), "No entry found for date: 2025-06-06")

    def test_update_entry(self):
        pass

    def test_delete_entry(self):
        pass