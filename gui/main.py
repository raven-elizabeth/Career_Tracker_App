from gui.root import Root
from gui.screens.home_screen import HomeScreen
from gui.screens.new_entry_screen import NewEntryScreen
from gui.screens.search_screen import SearchScreen


class App:
    def __init__(self):
        self._root = Root()
        self._home_screen = HomeScreen(
            self._root,
            on_new_entry=lambda: self.show_new_entry(),
            on_search=lambda: self.show_search()
        )
        self._search_screen = SearchScreen(
            self._root,
            on_home=lambda: self.show_home()
        )
        self._new_entry_screen = NewEntryScreen(self._root)

        self.show_home()

    def show_home(self):
        self._search_screen.pack_forget()
        self._home_screen.pack(fill="both", expand=True)

    def show_search(self):
        self._home_screen.pack_forget()
        self._search_screen.pack(fill="both", expand=True)

    def show_new_entry(self):
        pass

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
