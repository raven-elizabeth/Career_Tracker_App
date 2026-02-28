"""
This module defines the UpdateStrategy interface for updating client data in the GUI.
It uses the Strategy design pattern to allow for different update behaviors (e.g., replace vs. partial update)
without changing the client code that interacts with the strategy.
"""

from abc import ABC, abstractmethod


class UpdateStrategy(ABC):
    @abstractmethod
    def update(self, client, data):
        """Update the client data using the provided strategy."""
        pass