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

    def tearDown(self):
        self._test_dir.cleanup()

    def test_get_all_data(self):
        # Arrange
        entry = {
            "date": "2025-01-01",
            "work_contribution": "Completed unit tests for get route"
        }
        self.client.post("api/csv/entries", json=entry)

        # Act
        response = self.client.get("/api/csv/entries")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("2025-01-01,Completed unit tests for get route", response.get_json().get("data"))

    def test_get_data_by_date(self):
        # Arrange
        entry = {
            "date": "2025-01-02",
            "work_contribution": "Completed unit tests for get by date route"
        }
        entry2 = {
            "date": "2025-01-03",
            "work_contribution": "Completed unit tests for get by date route"
        }
        self.client.post("api/csv/entries", json=entry)
        self.client.post("api/csv/entries", json=entry2)

        # Act
        response = self.client.get("/api/csv/entries/2025-01-03")

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("2025-01-03, Completed unit tests for get by date route", response.get_json().get("data"))

    def test_post_data(self):
        # Arrange
        entry = {
            "date": "2024-12-31",
            "work_contribution": "Completed unit tests for post route"
        }

        # Act
        response = self.client.post("/api/csv/entries", json=entry)
        # The line below was modified with the help of GitHub Copilot to extract the date from the JSON response
        # entry is the key created by the json response for the post_data route
        # The empty dictionary is passed to avoid a key error on calling get('date') if entry is None
        date = response.get_json().get('entry', {}).get('date')

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(date, "2024-12-31")

