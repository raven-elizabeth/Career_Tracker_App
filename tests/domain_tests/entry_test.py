# This file contains unit tests for the Entry class in the domain layer.

import unittest
from domain.entry import Entry
from domain.fields import fields


class TestEntry(unittest.TestCase):
    def test_all_values_create_full_entry(self):
        # Arrange
        provided_values = {
            "date": "2025-12-31",
            "work_contribution": "Completed unit tests for domain layer",
            "learning": "Learned to use unittest framework for testing",
            "win": "Successfully ran all tests on first try",
            "challenge": "Had to learn how to use unittest framework",
            "next_steps": "Continue adding more tests and refactor code as needed"
        }

        # Act
        entry = Entry(**provided_values)

        # Assert
        self.assertEqual(entry.entry_dict, provided_values)

    def test_missing_optional_values_defaults_to_none(self):
        # Arrange
        provided_values = {"date": "2026-02-17", "work_contribution": "Completed unit tests for whole codebase"}
        expected = {value: provided_values.get(value) for value in fields}

        # Act
        entry = Entry(**provided_values)

        # Assert
        self.assertEqual(entry.entry_dict, expected)

    def test_no_date_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Entry()

        self.assertEqual(str(context.exception), "Unable to create entry: No date provided")

    def test_no_values_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Entry(date="2026-02-17")

        self.assertEqual("Unable to create entry: At least one value must not be empty", str(context.exception))