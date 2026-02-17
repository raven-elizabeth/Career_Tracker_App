from abc import ABC, abstractmethod


class DatabaseRepository(ABC):

    # Implement logic to save entry to the database (CREATE)
    @abstractmethod
    def save_entry(self, entry):
        pass

    # Implement logic to retrieve all entries from the database (READ)
    @abstractmethod
    def get_entries(self):
        pass

    # Implement logic to retrieve a specific entry by its ID (READ)
    @abstractmethod
    def get_entry_by_id(self, entry_id):
        pass

    # Implement logic to update an existing entry in the database (UPDATE)
    @abstractmethod
    def update_entry(self, entry_id, updated_entry):
        pass

    # Implement logic to delete an entry from the database (DELETE)
    @abstractmethod
    def delete_entry(self, entry_id):
        pass