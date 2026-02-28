"""
API client wrapper for the GUI layer.

Abstracts HTTP requests and error handling so that GUI code only deals with
domain objects and exceptions, not raw HTTP responses.
"""

import requests

from domain.dailyentry import DailyEntry
from gui.client_config import base_url


class ApiClient:
    BASE_URL = base_url

    @staticmethod
    def _get_error_message(response):
        """Safely extract an error message from a response, falling back to the status code if JSON is unavailable."""
        try:
            return response.json().get("error", "Unknown error")
        except Exception:
            return f"Unexpected response (status {response.status_code})"

    def get_entry_by_date(self, date):
        """Returns a DailyEntry object for the given date, or None if no entry exists.
        Raises ValueError if the file is unavailable or the server is unreachable."""
        try:
            response = requests.get(f"{self.BASE_URL}/{date}")
        except requests.exceptions.ConnectionError:
            raise ValueError("Could not connect to server. Make sure the API server is running.")
        if response.status_code == 200:
            data = response.json().get("data")
            return DailyEntry(**data)
        elif response.status_code == 404:
            return None
        else:
            raise ValueError(f"Failed to get entry: {self._get_error_message(response)}")

    def save_entry(self, entry_data):
        """Saves a new entry with the given data. Returns the saved entry data if successful."""
        response = requests.post(self.BASE_URL, json=entry_data)
        if response.status_code == 201:
            return response.json().get("data")
        else:
            raise ValueError(f"Failed to save entry: {self._get_error_message(response)}")

    def replace_entry(self, updated_data):
        """Replaces an existing entry with the given data. Returns the updated entry data if successful."""
        # Default date to empty string — passes any missing date error to the API to handle
        date = updated_data.get("date", "")
        response = requests.put(f"{self.BASE_URL}/{date}", json=updated_data)
        if response.status_code == 200:
            return response.json().get("data")
        else:
            raise ValueError(f"Failed to replace entry: {self._get_error_message(response)}")

    def partially_update_entry(self, update_data):
        """Partially updates an existing entry with the given data. Returns the updated entry data if successful."""
        date = update_data.get("date", "")
        response = requests.patch(f"{self.BASE_URL}/{date}", json=update_data)
        if response.status_code == 200:
            return response.json().get("data")
        else:
            raise ValueError(f"Failed to update entry: {self._get_error_message(response)}")

    def delete_entry(self, date):
        """Deletes the entry for the given date."""
        response = requests.delete(f"{self.BASE_URL}/{date}")
        if response.status_code != 204:
            raise ValueError(f"Failed to delete entry: {response.json().get('error', 'Unknown error')}")
