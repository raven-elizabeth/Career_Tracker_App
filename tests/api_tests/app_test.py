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

    def test_get_entry_nonexistent_file_returns_503_status_code(self):
        # Act
        response = self.client.get("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_get_entry_empty_file_returns_503_status_code(self):
        # Arrange
        with open(self._test_file_path, "w") as f:
            f.close()

        # Act
        response = self.client.get("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_get_nonexistent_entry_returns_not_found_response(self):
        # Act
        self.client.post("/api/csv/entries", json=self.entry)
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
        self.assertEqual(response.get_json().get("error"), "Invalid JSON body")

    def test_post_duplicate_entry_returns_conflict_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.post("/api/csv/entries", json=self.entry)

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertIn("Entry with date already exists", response.get_json().get("error"))

    def test_update_replace_entry_all_fields_returns_successful_response(self):
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
        response = self.client.put("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("message"), "Entry updated successfully")
        self.assertEqual(response.get_json().get("data"), updated_entry)

    def test_update_replace_nonexistent_entry_returns_not_found_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)
        updated_entry = {
            "date": "2025-01-04",
            "work_contribution": "Updated work contribution",
            "learning": "Added learning",
            "win": "",
            "challenge": "Added challenge",
            "next_steps": "Continue with testing"
        }

        # Act
        response = self.client.put("/api/csv/entries/2025-01-04", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("Update unsuccessful", response.get_json().get("error"))

    def test_update_replace_missing_fields_returns_bad_request_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "New work contribution"
        }

        # Act
        response = self.client.put("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Invalid JSON body", response.get_json().get("error"))

    def test_update_replace_nonexistent_file_returns_503_status_code(self):
        # Arrange
        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution",
            "learning": "Added learning",
            "win": "",
            "challenge": "Added challenge",
            "next_steps": "Continue with testing"
        }

        # Act
        response = self.client.put("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_update_replace_empty_file_returns_503_status_code(self):
        # Arrange
        with open(self._test_file_path, "w") as f:
            f.close()

        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution",
            "learning": "Added learning",
            "win": "",
            "challenge": "Added challenge",
            "next_steps": "Continue with testing"
        }

        # Act
        response = self.client.put("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_partial_update_entry_returns_successful_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution"
        }

        expected_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution",
            "learning": "",
            "win": "",
            "challenge": "",
            "next_steps": "Continue with testing"
        }

        # Act
        response = self.client.patch("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("message"), "Entry partially updated successfully")
        self.assertEqual(response.get_json().get("data"), expected_entry)

    def test_partial_update_nonexistent_entry_returns_not_found_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)
        updated_entry = {
            "date": "2025-01-04",
            "work_contribution": "Updated work contribution"
        }

        # Act
        response = self.client.patch("/api/csv/entries/2025-01-04", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("Partial update unsuccessful", response.get_json().get("error"))

    def test_partial_update_entry_with_empty_fields_does_not_overwrite_existing_data(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": ""
        }

        expected_entry = {
            "date": "2025-01-02",
            "work_contribution": "Completed unit tests for Flask routes",
            "learning": "",
            "win": "",
            "challenge": "",
            "next_steps": "Continue with testing"
        }

        # Act
        response = self.client.patch("/api/csv/entries/2025-01-02", json=updated_entry)
        entry = self.client.get("/api/csv/entries/2025-01-02").get_json()

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No valid fields provided for update", response.get_json().get("error"))
        self.assertEqual(entry.get("data"), expected_entry)

    def test_partial_update_nonexistent_file_returns_503_status_code(self):
        # Arrange
        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution"
        }

        # Act
        response = self.client.patch("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_partial_update_empty_file_returns_503_status_code(self):
        # Arrange
        with open(self._test_file_path, "w") as f:
            f.close()

        updated_entry = {
            "date": "2025-01-02",
            "work_contribution": "Updated work contribution"
        }

        # Act
        response = self.client.patch("/api/csv/entries/2025-01-02", json=updated_entry)

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_delete_entry_returns_successful_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("message"), "Entry deleted successfully")

    def test_delete_entry_empty_file_returns_503_status_code(self):
        # Arrange
        with open(self._test_file_path, "w") as f:
            f.close()

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_delete_entry_nonexistent_file_returns_503_status_code(self):
        # Act
        response = self.client.delete("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_delete_nonexistent_entry_returns_not_found_response(self):
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-04")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("error"), "Delete unsuccessful")