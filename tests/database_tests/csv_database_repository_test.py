# This file contains unit tests for the CsvDatabaseRepository class.
# The tests use the AAA (Arrange, Act, Assert) pattern to structure the test cases.

import csv
from os import path
import unittest
import tempfile
from database.csv_database_repository import CsvDatabaseRepository
from domain.entry import Entry


class TestCsvDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path = path.join(self.test_dir.name, "test_entries.csv")
        self.repo = CsvDatabaseRepository(file_path=self.file_path)
        self.entry = Entry(date="2025-06-04", work_contribution="Completed unit tests for whole codebase")
        self.expected = {
            "date": "2025-06-04",
            "work_contribution": "Completed unit tests for whole codebase",
            "learning": "",
            "win": "",
            "challenge": "",
            "next_steps": ""
        }

    def test_save_entry(self):
        # Act
        self.repo.save_entry(self.entry)

        # Assert
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 1)

            self.assertEqual(rows[0], self.expected)

    def test_get_entries(self):
        pass

    def test_get_entry_by_date(self):
        pass

    def test_update_entry(self):
        pass

    def test_delete_entry(self):
        pass