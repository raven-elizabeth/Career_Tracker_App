"""
Unit tests for the ApiClient class in gui.client.

Uses mocking to simulate API responses without a running server.
Each test uses @patch to replace the relevant requests method with a
MagicMock configured to return specific status codes and JSON payloads,
covering success, not-found, and error scenarios.

AI was used to help write the initial test structure; tests were then
manually edited and commented for clarity.
"""

import unittest
from unittest.mock import patch, MagicMock

from gui.api_client.client import ApiClient

# Reusable sample entry data representing a full, valid entry.
# Not using setUp since this is the only test data needed, making it
# simpler to define as a constant.
SAMPLE_ENTRY = {
    "date": "2024-01-01",
    "work_contribution": "Worked on project",
    "learning": "Learned testing",
    "win": "Fixed a bug",
    "challenge": "Debugging",
    "next_steps": "Write more tests",
}


class ClientTest(unittest.TestCase):

    @patch("gui.api_client.client.requests.get")
    def test_get_entry_by_date_returns_entry(self, mock_get):
        """Test that get_entry_by_date returns a DailyEntry object when the
        API responds with a valid entry."""
        # Arrange: Configure the mock to return a 200 response with the
        # sample entry inside a "data" key
        mock_get.return_value = MagicMock(
            status_code=200, json=lambda: {"data": SAMPLE_ENTRY}
        )

        # Act
        entry = ApiClient().get_entry_by_date("2024-01-01")

        # Assert
        self.assertIsNotNone(entry)
        self.assertEqual(entry.entry_dict["date"], "2024-01-01")

    @patch("gui.api_client.client.requests.get")
    def test_get_entry_by_date_not_found_returns_none(self, mock_get):
        """Test that get_entry_by_date returns None when the API responds
        with a 404 Not Found."""
        # Arrange: Simulate a 404 response — the entry does not exist
        mock_get.return_value = MagicMock(
            status_code=404, json=lambda: {"error": "Not found"}
        )

        # Act
        entry = ApiClient().get_entry_by_date("2024-01-01")

        # Assert
        self.assertIsNone(entry)

    @patch("gui.api_client.client.requests.get")
    def test_get_entry_by_date_unexpected_error_raises(self, mock_get):
        """Test that get_entry_by_date raises a ValueError when the API
        responds with an unexpected error status."""
        # Arrange: Simulate a 500 server error — any non-200/404 status
        # should raise a ValueError
        mock_get.return_value = MagicMock(
            status_code=500, json=lambda: {"error": "Server error"}
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().get_entry_by_date("2024-01-01")

    @patch("gui.api_client.client.requests.get")
    def test_get_entry_by_date_service_unavailable_raises(self, mock_get):
        """Test that get_entry_by_date raises a ValueError when the API
        responds with 503 Service Unavailable."""
        # Arrange: Simulate a 503 — file deleted or emptied mid-session
        mock_get.return_value = MagicMock(
            status_code=503, json=lambda: {"error": "File unavailable"}
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().get_entry_by_date("2024-01-01")

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().get_entry_by_date("2024-01-01")

    @patch("gui.api_client.client.requests.post")
    def test_save_entry_returns_data(self, mock_post):
        """Test that save_entry returns the saved entry data when the API
        responds with a 201 Created."""
        # Arrange: Simulate a successful 201 Created response with the
        # saved entry data
        mock_post.return_value = MagicMock(
            status_code=201, json=lambda: {"data": SAMPLE_ENTRY}
        )

        # Act
        result = ApiClient().save_entry(SAMPLE_ENTRY)

        # Assert
        self.assertEqual(result, SAMPLE_ENTRY)

    @patch("gui.api_client.client.requests.post")
    def test_save_entry_failure_raises(self, mock_post):
        """Test that save_entry raises a ValueError when the API responds
        with an error status."""
        # Arrange: Simulate a 400 Bad Request — e.g. missing required fields
        mock_post.return_value = MagicMock(
            status_code=400, json=lambda: {"error": "Bad request"}
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().save_entry(SAMPLE_ENTRY)

    @patch("gui.api_client.client.requests.put")
    def test_replace_entry_returns_data(self, mock_put):
        """Test that replace_entry returns the updated entry data when the
        API responds with a 200 OK."""
        # Arrange: Simulate a successful 200 OK response after a full
        # replacement
        mock_put.return_value = MagicMock(
            status_code=200, json=lambda: {"data": SAMPLE_ENTRY}
        )

        # Act
        result = ApiClient().replace_entry(SAMPLE_ENTRY)

        # Assert
        self.assertEqual(result, SAMPLE_ENTRY)

    @patch("gui.api_client.client.requests.put")
    def test_replace_entry_not_found_raises(self, mock_put):
        """Test that replace_entry raises a ValueError when the API responds
        with a 404 Not Found."""
        # Arrange: Simulate a 404 — trying to replace an entry that does
        # not exist
        mock_put.return_value = MagicMock(
            status_code=404, json=lambda: {"error": "Not found"}
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().replace_entry(SAMPLE_ENTRY)

    @patch("gui.api_client.client.requests.patch")
    def test_update_entry_returns_data(self, mock_patch):
        """Test that update_entry returns the updated entry data when the
        API responds with a 200 OK."""
        # Arrange: Simulate a successful 200 OK response after a partial
        # update
        mock_patch.return_value = MagicMock(
            status_code=200, json=lambda: {"data": SAMPLE_ENTRY}
        )

        # Act
        result = ApiClient().partially_update_entry(SAMPLE_ENTRY)

        # Assert
        self.assertEqual(result, SAMPLE_ENTRY)

    @patch("gui.api_client.client.requests.patch")
    def test_update_entry_failure_raises(self, mock_patch):
        """Test that update_entry raises a ValueError when the API responds
        with an error status."""
        # Arrange: Simulate a 400 Bad Request — e.g. all fields are empty
        mock_patch.return_value = MagicMock(
            status_code=400, json=lambda: {"error": "Bad request"}
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().partially_update_entry(SAMPLE_ENTRY)

    @patch("gui.api_client.client.requests.delete")
    def test_delete_entry_succeeds(self, mock_delete):
        """Test that delete_entry completes without raising when the API
        responds with a 204 No Content."""
        # Arrange: Simulate a successful 204 No Content response —
        # deletion has no response body
        mock_delete.return_value = MagicMock(status_code=204)

        # Act
        response = ApiClient().delete_entry("2024-01-01")

        # Assert
        # Added this myself - AI did not include an assert as just wanted
        # to check no exception is raised, but it's good to be explicit
        # about the expected return value
        self.assertEqual(None, response)

    @patch("gui.api_client.client.requests.delete")
    def test_delete_entry_not_found_raises(self, mock_delete):
        """Test that delete_entry raises a ValueError when the API responds
        with a 404 Not Found."""
        # Arrange: Simulate a 404 — trying to delete an entry that does
        # not exist
        mock_delete.return_value = MagicMock(
            status_code=404, json=lambda: {"error": "Not found"}
        )

        # Act & Assert
        with self.assertRaises(ValueError):
            ApiClient().delete_entry("2024-01-01")


if __name__ == "__main__":
    unittest.main()
