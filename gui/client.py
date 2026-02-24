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
