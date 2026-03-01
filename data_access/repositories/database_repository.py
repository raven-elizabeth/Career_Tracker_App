"""
Defines the DatabaseRepository abstract base class.

All concrete repository implementations must implement the CRUD methods defined here,
ensuring a consistent interface regardless of the underlying storage mechanism.
"""

from abc import ABC, abstractmethod


class DatabaseRepository(ABC):

    @abstractmethod
    def save_entry(self, entry):
        """Implement logic to save entry to the data_access (CREATE)"""
        pass

    @abstractmethod
    def get_entry_by_date(self, entry_date):
        """Implement logic to retrieve a specific entry by its date (READ)"""
        pass

    @abstractmethod
    def replace_entry(self, entry_date, updated_entry):
        """Implement logic to replace an existing entry in the data_access (UPDATE: PUT)"""
        pass

    @abstractmethod
    def partially_update_entry(self, update_request):
        """Implement logic to partially update an existing entry in the data_access (UPDATE: PATCH)"""
        pass

    @abstractmethod
    def delete_entry(self, entry_date):
        """Implement logic to delete an entry from the data_access (DELETE)"""
        pass
