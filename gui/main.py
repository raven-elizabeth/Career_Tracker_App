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
        self._search_screen = SearchScreen(
            self._root,
            on_home=self.show_home,
            on_date=self._api_client.get_entry_by_date
        )
        self._new_entry_screen = NewEntryScreen(
            self._root,
            on_home=self.show_home,
            on_valid_save=self._api_client.save_entry,
            on_date=self._api_client.get_entry_by_date,
            on_full_replace=self._api_client.replace_entry,
            on_partial_update=self._api_client.update_entry
        )

        self.show_home()

    def show_home(self):
        self._search_screen.pack_forget()
        self._new_entry_screen.pack_forget()
        # fill=both fills the window horizontally and vertically; expand=True allows the screen to resize with the window
        self._home_screen.pack(fill="both", expand=True)

    def show_search(self):
        self._home_screen.pack_forget()
        self._search_screen.pack(fill="both", expand=True)

    def show_new_entry(self):
        self._home_screen.pack_forget()
        self._new_entry_screen.refresh()
        self._new_entry_screen.pack(fill="both", expand=True)

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
