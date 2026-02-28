"""
This is the main application file that connects all the app components together.
It initializes the API client, creates the main window (Root),
and sets up the different screens (HomeScreen, NewEntryScreen, SearchScreen).
The App class manages the navigation between screens and handles interactions with the API client for CRUD operations.
It cannot be run without the Flask API server running, so make sure to run app.py first.
"""

from gui.client import ApiClient
from gui.root import Root
from gui.screens.home_screen import HomeScreen
from gui.screens.new_entry_screen import NewEntryScreen
from gui.screens.search_screen import SearchScreen


class App:
    def __init__(self):
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
            on_home=self.show_home,
            on_valid_save=self._api_client.save_entry,
            on_date=self._api_client.get_entry_by_date,
            on_full_replace=self._api_client.replace_entry,
            on_partial_update=self._api_client.update_entry
        )
        self._search_screen = SearchScreen(
            self._root,
            on_home=self.show_home,
            on_date=self._api_client.get_entry_by_date,
            on_edit=self._edit_entry,
            on_delete=self._api_client.delete_entry
        )

        self.show_home()

    def show_home(self):
        self._search_screen.pack_forget()
        self._new_entry_screen.pack_forget()
        # fill=both fills the window horizontally and vertically; expand=True allows the screen to resize with the window
        self._home_screen.pack(fill="both", expand=True)

    def show_search(self):
        self._home_screen.pack_forget()
        self._search_screen.refresh_display()
        self._search_screen.pack(fill="both", expand=True)

    def show_new_entry(self):
        self._home_screen.pack_forget()
        self._new_entry_screen.refresh_screen()
        self._new_entry_screen.pack(fill="both", expand=True)

    def _edit_entry(self, entry_dict):
        """Navigate to new entry screen pre-populated with the selected entry's date."""
        date = entry_dict.get("date")
        self._search_screen.pack_forget()
        self._new_entry_screen.refresh_screen(date=date)
        self._new_entry_screen.pack(fill="both", expand=True)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
