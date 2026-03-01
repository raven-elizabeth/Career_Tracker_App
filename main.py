"""
This is the main application file that connects all the app components together.
It initializes the API client, creates the main window (Root),
and sets up the different screens (HomeScreen, NewEntryScreen, SearchScreen).
The App class manages the navigation between screens and handles interactions with the API client for CRUD operations.
It cannot be run without the Flask API server running, so make sure to run api.py first.
"""

from data_access.api_client.client import ApiClient
from gui.root import Root
from gui.screens.home_screen import HomeScreen
from gui.screens.new_entry_screen import NewEntryScreen
from gui.screens.search_screen import SearchScreen
from logs.logging_config import get_logger


class App:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._logger.info("Starting Career Tracker App")
        self._api_client = ApiClient()

        self._root = Root()
        self._home_screen = HomeScreen(
            self._root,
            on_new_entry=self.show_new_entry,
            on_search=self.show_search
        )
        # NewEntryScreen must be created before SearchScreen so _edit_entry can reference it
        self._new_entry_screen = NewEntryScreen(
            self._root,
            client=self._api_client,
            on_home=self.show_home
        )
        self._search_screen = SearchScreen(
            self._root,
            client=self._api_client,
            on_home=self.show_home,
            on_edit=self._edit_entry
        )

        self.show_home()

    def _show_screen(self, screen):
        """Helper to hide all screens and display the given screen."""
        for s in (self._home_screen, self._search_screen, self._new_entry_screen):
            s.pack_forget()
        # fill=both fills the window horizontally and vertically; expand=True allows the screen to resize with the window
        screen.pack(fill="both", expand=True)

    def show_home(self):
        """Display the home screen."""
        self._logger.info("Navigating to home screen")
        self._show_screen(self._home_screen)

    def show_search(self):
        """Refresh the search display and show the search screen."""
        self._logger.info("Navigating to search screen")
        self._search_screen.refresh_display()
        self._show_screen(self._search_screen)

    def show_new_entry(self):
        """Reset the new entry screen to today's date and show it."""
        self._logger.info("Navigating to new entry screen")
        self._new_entry_screen.refresh_screen()
        self._show_screen(self._new_entry_screen)

    def _edit_entry(self, entry_dict):
        """Navigate to the new entry screen pre-populated with the selected entry's date."""
        date = entry_dict.get("date")
        self._logger.info("Navigating to edit entry for date: %s", date)
        self._new_entry_screen.refresh_screen(date=date)
        self._show_screen(self._new_entry_screen)

    def run(self):
        """Start the Tkinter main event loop."""
        self._root.mainloop()


# Note that you MUST run the Flask API server (api.api.py) before running this app, otherwise it will not work.
if __name__ == "__main__":
    app = App()
    app.run()
