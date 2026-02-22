import datetime
from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._make_calendar()
        self.display_frame = self._create_frame(row=2)
        self.inner_frame = self._create_inner_frame(self.display_frame)
        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )

    def _make_responsive(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top padding
        self.grid_rowconfigure(1, weight=2)  # Calendar row
        self.grid_rowconfigure(2, weight=6)  # Display frame row
        self.grid_rowconfigure(3, weight=1)  # Bottom padding

    def _make_calendar(self):
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self.calendar.grid(row=1, column=0, columnspan=2, padx=60, sticky="nsew")


if __name__ == "__main__":
    from gui.root import Root
    root = Root()
    search_screen = SearchScreen(root)
    search_screen.pack(fill="both", expand=True)
    root.mainloop()
