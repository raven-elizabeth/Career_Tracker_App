"""This module defines the ReplaceStrategy class, which implements the UpdateStrategy interface.
It uses the replace_entry method of the client to replace an existing entry with new data (PUT)."""

from gui.screens.strategies.update_strategy import UpdateStrategy


class ReplaceStrategy(UpdateStrategy):
    def update(self, client, data):
        """Replace the client data using the client's replace_entry method."""
        return client.replace_entry(data)
