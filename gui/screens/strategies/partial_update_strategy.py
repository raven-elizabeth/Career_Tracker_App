"""
This module contains the PartialUpdateStrategy class, which implements the
UpdateStrategy interface. It uses the client's partially_update_entry
method to send a PATCH request to the API.
"""

from gui.screens.strategies.update_strategy import UpdateStrategy


class PartialUpdateStrategy(UpdateStrategy):
    def update(self, client, data):
        """Partially update the client data using the client's
        partially_update_entry method."""
        return client.partially_update_entry(data)