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

    def replace_entry(self, updated_data):
        date = updated_data.get("date")
        response = requests.put(f"{self.BASE_URL}/{date}", json=updated_data)
        if response.status_code == 200:
            return response.json().get("data")
        else:
            raise ValueError(f"Failed to update entry: {response.json().get('error', 'Unknown error')}")

    def update_entry(self, update_data):
        date = update_data.get("date")
        response = requests.patch(f"{self.BASE_URL}/{date}", json=update_data)
        if response.status_code == 200:
            return response.json().get("data")
        else:
            raise ValueError(f"Failed to update entry: {response.json().get('error', 'Unknown error')}")

    def delete_entry(self, date):
        response = requests.delete(f"{self.BASE_URL}/{date}")
        if response.status_code != 204:
            raise ValueError(f"Failed to delete entry: {response.json().get('error', 'Unknown error')}")

