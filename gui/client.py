import requests

from domain.dailyentry import DailyEntry


class ApiClient:
    BASE_URL = "http://127.0.0.1:5000/api/csv/entries"

    def get_entry_by_date(self, date):
        response = requests.get(f"{self.BASE_URL}/{date}")
        if response.status_code == 200:
            data = response.json().get("data")
            return DailyEntry(**data)
        return None

    def save_entry(self, entry_data):
        response = requests.post(self.BASE_URL, json=entry_data)
        if response.status_code == 201:
            return response.json().get("data")
        else:
            raise ValueError(f"Failed to save entry: {response.json().get('error', 'Unknown error')}")
