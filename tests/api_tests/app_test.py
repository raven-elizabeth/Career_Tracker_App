import unittest
import tempfile
import os
from api.app import API
from database.csv_database_repository import CsvDatabaseRepository


class TestAPI(unittest.TestCase):
    def setUp(self):
        self._test_dir = tempfile.TemporaryDirectory()
        self._test_file_path = os.path.join(self._test_dir.name, "test_entries.csv")
        self._repo = CsvDatabaseRepository(file_path=self._test_file_path)
        self.api = API(repository=self._repo)
        self.client = self.api.app.test_client()

        self.entry = {
            "date": "2025-01-02",
            "work_contribution": "Completed unit tests for Flask routes",
            "next_steps": "Continue with testing"
        }

        self.expected = {
            "date": "2025-01-02",
            "work_contribution": "Completed unit tests for Flask routes",
            "learning": "",
            "win": "",
            "challenge": "",
            "next_steps": "Continue with testing"
        }

    def tearDown(self):
        self._test_dir.cleanup()

    def test_get_entry_by_date_returns_successful_response(self):
        # Arrange
        entry2 = {
            "date": "2025-01-03",
            "work_contribution": "Completed unit tests for get by date route"
        }
        self.client.post("/api/csv/entries", json=self.entry)
        self.client.post("/api/csv/entries", json=entry2)

        # Act
        response = self.client.get("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("message"), "Entry retrieved successfully")
        self.assertEqual(response.get_json().get("data"), self.expected)

    def test_get_nonexistent_entry_returns_not_found_response(self):
        # Act
        response = self.client.get("/api/csv/entries/2025-01-04")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("error"), "No entry found for date: 2025-01-04")

    def test_post_entry_returns_successful_response(self):
        # Act
        response = self.client.post("/api/csv/entries", json=self.entry)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json().get("message"), "Entry saved successfully")
        self.assertEqual(response.get_json().get("data"), self.expected)

    def test_post_entry_no_json_returns_bad_request_response(self):
        # Act
        response = self.client.post("/api/csv/entries", json={})

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get("error"), "Save unsuccessful")

    def test_update_entry_all_fields_returns_successful_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution",
            "learning": "Added learning",
            "win": "",
            "challenge": "Added challenge",
            "next_steps": "Continue with testing"
        }

        # Act
        self.client.put("/api/csv/entries/2025-01-02", json=updated_entry)
        response = self.client.get("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("message"), "Entry retrieved successfully")
        self.assertEqual(response.get_json().get("data"), updated_entry)

    def test_update_nonexistent_entry_returns_not_found_response(self):
        # Arrange
        updated_entry = {
            "date": "2025-01-04",
            "work_contribution": "Updated work contribution",
            "learning": "Added learning",
            "challenge": "Added challenge"
        }

        # Act
        response = self.client.put("/api/csv/entries/2025-01-04", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("error"), "Update unsuccessful")

    def test_delete_entry_returns_successful_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("message"), "Entry deleted successfully")

    def test_delete_nonexistent_entry_returns_not_found_response(self):
        # Act
        response = self.client.delete("/api/csv/entries/2025-01-04")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("error"), "Delete unsuccessful")