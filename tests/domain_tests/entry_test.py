import unittest
from domain.entry import Entry
from domain.fields import fields


class TestEntry(unittest.TestCase):
    def test_missing_optional_values_defaults_to_none(self):
        provided_values = {"date": "2026-02-17", "work_contribution": "Completed unit tests for whole codebase"}
        entry = Entry(**provided_values)
        expected = {value: provided_values.get(value) for value in fields}
        self.assertEqual(entry.entry_dict, expected)

    def test_no_date_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Entry()

        self.assertEqual(str(context.exception), "Unable to create entry: No date provided")

    def test_no_values_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Entry(date="2026-02-17")

        self.assertEqual("Unable to create entry: At least one value must not be empty", str(context.exception))