"""
This file defines unit tests for the API class in the api.api module.
The tests cover all CRUD operations for daily entries, including successful cases and various error scenarios.
The tests use a temporary directory and file to ensure isolation and avoid side effects on the actual data.
The tests verify that the API returns the correct status codes and response data for each scenario,
ensuring that the API behaves as expected under different conditions.
"""

import os
import tempfile
import unittest

from api.api import API
from database.csv_database_repository import CsvDatabaseRepository


class TestAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary directory and file for testing, and initialize the API
        with a CsvDatabaseRepository. Set up sample entry data and expected response
        data for use in the tests.
        """

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
        """Clean up the temporary directory and file after each test."""
        self._test_dir.cleanup()

    def test_get_entry_by_date_returns_successful_response(self):
        """Test that a GET request to retrieve an entry by date returns a successful response with the correct data."""
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

    def test_get_entry_empty_file_returns_service_unavailable_status_code(self):
        """Test that GET request to retrieve entry by date returns 503 when the file is empty."""
        # Arrange
        with open(self._test_file_path, "w") as f:
            f.close()

        # Act
        response = self.client.get("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_get_nonexistent_entry_returns_no_content_response(self):
        """Test that GET request to retrieve entry by date returns a 404 status code when the entry does not exist."""
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.get("/api/csv/entries/2025-01-04")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json().get("message"), "No entry found for date: 2025-01-04")

    def test_post_entry_returns_successful_response(self):
        """Test that a POST request to create a new entry returns a successful response with the correct data."""
        # Act
        response = self.client.post("/api/csv/entries", json=self.entry)

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json().get("message"), "Entry saved successfully")
        self.assertEqual(response.get_json().get("data"), self.expected)

    def test_post_entry_no_json_returns_bad_request_response(self):
        """Test that a POST request to create new entry returns a bad request response when no JSON body is provided."""
        # Act
        response = self.client.post("/api/csv/entries", json={})

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json().get("error"), "Invalid JSON body")

    def test_post_duplicate_entry_returns_conflict_response(self):
        """Test that a POST request to create an entry with a date that already exists returns a conflict response."""
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.post("/api/csv/entries", json=self.entry)

        # Assert
        self.assertEqual(response.status_code, 409)
        self.assertIn("Entry with date already exists", response.get_json().get("error"))

    def test_update_replace_entry_all_fields_returns_successful_response(self):
        """Test PUT request to update existing entry with all fields returns successful response with updated data."""
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
        """Test that a PUT request to update an entry that does not exist returns a not found response."""
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
        """Test that a PUT request to update an entry with missing fields returns a bad request response."""
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
        self.assertEqual(
            "Invalid data for Entry class: PUT request requires replacement data for all fields in the Entry class",
            response.get_json().get("error")
        )

    def test_update_replace_empty_file_returns_service_unavailable_status_code(self):
        """Test that PUT request to update entry returns service unavailable status code when file is empty."""
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
        """Test that PATCH request to partially update existing entry returns successful response with updated data."""
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
        """Test that PATCH request to partially update entry that does not exist returns a not found response."""
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
        """Test that PATCH request to partially update entry with empty fields does not overwrite existing data 
        with empty values."""
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
        self.assertEqual(
            "Invalid data for Entry class: Unable to create entry: At least one value must not be empty",
            response.get_json().get("error")
        )
        self.assertEqual(entry.get("data"), expected_entry)

    def test_partial_update_empty_file_returns_service_unavailable_status_code(self):
        """Test that PATCH request to partially update entry returns service unavailable status code 
        when file is empty."""
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
        """Test that a DELETE request to delete an entry by date returns a successful response with no content."""
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.get_json())

    def test_delete_entry_empty_file_returns_service_unavailable_status_code(self):
        """Test that a DELETE request to delete an entry by date returns a service unavailable status code 
        when the file is empty."""
        # Arrange
        with open(self._test_file_path, "w") as f:
            f.close()

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json().get("error"), "File unavailable")

    def test_delete_nonexistent_entry_returns_not_found_response(self):
        """Test that a DELETE request to delete an entry by date returns a not found response 
        when the entry does not exist."""
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)

        # Act
        response = self.client.delete("/api/csv/entries/2025-01-04")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("Delete unsuccessful", response.get_json().get("error"))

    def test_deleted_entry_is_no_longer_retrievable(self):
        """Test that an entry that has been deleted is no longer retrievable via GET request."""
        # Arrange
        self.client.post("/api/csv/entries", json=self.entry)
        self.client.delete("/api/csv/entries/2025-01-02")

        # Act
        response = self.client.get("/api/csv/entries/2025-01-02")

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertIn("No entry found for date: 2025-01-02", response.get_json().get("message"))