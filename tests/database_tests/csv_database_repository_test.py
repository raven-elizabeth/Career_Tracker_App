# This file contains unit tests for the CsvDatabaseRepository class.
# The tests use the AAA (Arrange, Act, Assert) pattern to structure the test cases.

import csv
import unittest
from domain.entry import Entry
from tests.test_data import test_repository, test_dir


class TestCsvDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = test_repository
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
        test_dir.cleanup()

    def test_save_entry(self):
        # Act
        self.repo.save_entry(self.entry)

        # Assert
        with open(self.repo.file_path, 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0], self.expected)

    def test_get_entry_by_date(self):
        # Arrange
        self.repo.save_entry(self.entry)
        entry_two = Entry(
            date="2025-06-05",
            work_contribution="Completed unit tests for get_entries method",
            learning="Discovered how to use temp file"
        )
        self.repo.save_entry(entry_two)

        # Act
        data_one = self.repo.get_entry_by_date("2025-06-04")
        data_two = self.repo.get_entry_by_date("2025-06-05")

        # Assert
        self.assertTrue(data_one)
        self.assertEqual(data_one.entry_dict, self.expected)
        self.assertTrue(data_two)
        self.assertEqual(data_two.entry_dict, {
            "date": "2025-06-05",
            "work_contribution": "Completed unit tests for get_entries method",
            "learning": "Discovered how to use temp file",
            "win": "",
            "challenge": "",
            "next_steps": ""
        })

    def test_update_entry(self):
        pass

    def test_delete_entry(self):
        pass