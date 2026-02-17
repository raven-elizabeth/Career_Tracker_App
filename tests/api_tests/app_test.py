from api.app import API
from tests.test_data import test_repository, test_dir
import unittest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = API(repository=test_repository)
        self.client = self.api.app.test_client()

    def tearDown(self):
        test_dir.cleanup()

    def test_get_data(self):
        # Act
        response = self.client.get('/api/csv/entries')

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_post_data(self):
        # Arrange
        entry = {
            "date": "2024-12-31",
            "work_contribution": "Completed unit tests for post route"
        }

        # Act
        response = self.client.post('/api/csv/entries', json=entry)
        date = response.get_json().get('entry', {}).get('date')

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(date, "2024-12-31")

