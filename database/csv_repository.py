from database.database_repository import DatabaseRepository


class CsvRepository(DatabaseRepository):
    def __init__(self, file_path="entries.csv"):
        super().__init__()
        self.file_path = file_path

    def save_entry(self, entry):
        # Implement logic to save entry to the CSV file
        pass

    def get_entries(self):
        # Implement logic to retrieve all entries from the CSV file
        pass

    def get_entry_by_id(self, entry_id):
        # Implement logic to retrieve a specific entry by its ID from the CSV file
        pass

    def update_entry(self, entry_id, updated_entry):
        # Implement logic to update an existing entry in the CSV file
        pass

    def delete_entry(self, entry_id):
        # Implement logic to delete an entry from the CSV file
        pass