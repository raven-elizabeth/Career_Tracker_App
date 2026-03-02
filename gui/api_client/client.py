"""
API client wrapper for the GUI layer.

Abstracts HTTP requests and error handling so that GUI code only deals with
domain objects and exceptions, not raw HTTP responses.
"""

import requests

from domain.dailyentry import DailyEntry
from gui.api_client.client_config import base_url
from api.http_status_codes import (
    HTTP_OK,
    HTTP_CREATED,
    HTTP_NO_CONTENT,
    HTTP_NOT_FOUND,
)


class ApiClient:
    # Sets a default timeout in seconds for all requests to prevent
    # hanging if the server is unresponsive
    REQUEST_TIMEOUT = 10

    @staticmethod
    def _get_error_message(response):
        """Safely extract an error message from a response, falling back to
        the status code if JSON is unavailable."""
        try:
            return response.json().get("error", "Unknown error")
        except Exception as e:
            return (
                f"Unexpected response (status {response.status_code}), {e}"
            )

    def get_entry_by_date(self, date):
        """Returns a DailyEntry object for the given date, or None if no
        entry exists.
        Raises ValueError if the file is unavailable or the server is
        unreachable."""
        try:
            response = requests.get(
                f"{base_url}/{date}",
                timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Could not connect to server. "
                "Make sure the API server is running."
            )
        if response.status_code == HTTP_OK:
            data = response.json().get("data")
            return DailyEntry(**data)
        elif response.status_code == HTTP_NOT_FOUND:
            return None
        else:
            raise ValueError(
                f"Failed to get entry: {self._get_error_message(response)}"
            )

    def save_entry(self, entry_data):
        """Saves a new entry with the given data.
        Returns the saved entry data if successful."""
        try:
            response = requests.post(
                base_url,
                json=entry_data,
                timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Could not connect to server. "
                "Make sure the API server is running."
            )
        if response.status_code == HTTP_CREATED:
            return response.json().get("data")
        else:
            raise ValueError(
                f"Failed to save entry: {self._get_error_message(response)}"
            )

    def replace_entry(self, updated_data):
        """Replaces an existing entry with the given data.
        Returns the updated entry data if successful."""
        date = updated_data.get("date")
        if not date:
            raise ValueError("Date is required for replacement")

        try:
            response = requests.put(
                f"{base_url}/{date}",
                json=updated_data,
                timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Could not connect to server. "
                "Make sure the API server is running."
            )
        if response.status_code == HTTP_OK:
            return response.json().get("data")
        else:
            raise ValueError(
                f"Failed to replace entry: "
                f"{self._get_error_message(response)}"
            )

    def partially_update_entry(self, update_data):
        """Partially updates an existing entry with the given data.
        Returns the updated entry data if successful."""
        date = update_data.get("date")
        if not date:
            raise ValueError("Date is required for partial update")

        try:
            response = requests.patch(
                f"{base_url}/{date}",
                json=update_data,
                timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Could not connect to server. "
                "Make sure the API server is running."
            )
        if response.status_code == HTTP_OK:
            return response.json().get("data")
        else:
            raise ValueError(
                f"Failed to update entry: "
                f"{self._get_error_message(response)}"
            )

    def delete_entry(self, date):
        """Deletes the entry for the given date."""
        try:
            response = requests.delete(
                f"{base_url}/{date}",
                timeout=self.REQUEST_TIMEOUT
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                "Could not connect to server. "
                "Make sure the API server is running."
            )
        if response.status_code != HTTP_NO_CONTENT:
            raise ValueError(
                f"Failed to delete entry: "
                f"{self._get_error_message(response)}"
            )
