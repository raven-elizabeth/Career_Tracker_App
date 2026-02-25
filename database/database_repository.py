# This module defines the DatabaseRepository interface, which specifies the CRUD methods for interacting with the database.

from abc import ABC, abstractmethod


class DatabaseRepository(ABC):

    # Implement logic to save entry to the database (CREATE)
    @abstractmethod
    def save_entry(self, entry):
        pass

    # Implement logic to retrieve a specific entry by its date (READ)
    @abstractmethod
    def get_entry_by_date(self, entry_date):
        pass

    # Implement logic to update an existing entry in the database (UPDATE: PUT)
    @abstractmethod
    def replace_entry(self, entry_date, updated_entry):
        pass

    # Implement logic to partially update an existing entry in the database (UPDATE: PATCH)
    @abstractmethod
    def partially_update_entry(self, update_request):
        pass

    # Implement logic to delete an entry from the database (DELETE)
    @abstractmethod
    def delete_entry(self, entry_date):
        pass