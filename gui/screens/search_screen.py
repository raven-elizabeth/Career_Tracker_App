import datetime
from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        column_weights = {0: 1, 1: 1}
        # Row weights set to create more space for calendar and display frame, with padding rows at top, middle, and bottom
        # Display frame has more weight than calendar to allow for more space to show entry data
        row_weights = {0: 1, 1: 2, 2: 6, 3: 1}
        self._make_responsive(column_weights, row_weights)

        self._make_calendar()
        self.display_frame = self._create_frame(row=2)
        self.inner_frame = self._create_inner_frame(self.display_frame)
        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )

    def _make_calendar(self):
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self.calendar.grid(row=1, column=0, columnspan=2, padx=60, sticky="nsew")


if __name__ == "__main__":
    from gui.root import Root
    root = Root()
    search_screen = SearchScreen(root)
    search_screen.pack(fill="both", expand=True)
    root.mainloop()
