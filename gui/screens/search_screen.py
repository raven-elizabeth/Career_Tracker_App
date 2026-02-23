import datetime
from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    def __init__(self, *args, on_valid_date=None, on_home=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_valid_date = on_valid_date
        self._on_home = on_home

        column_weights = {0: 1, 1: 1}
        # Row weights set; display frame has more weight than calendar to show more entry data.
        row_weights = {0: 1, 1: 2, 2: 6, 3: 1, 4: 1}
        self._configure_responsive_grid(column_weights, row_weights)

        self._setup_calendar()
        self._setup_display_frame()
        self._add_home_button()

    def _setup_calendar(self):
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self.calendar.grid(row=1, column=0, columnspan=2, padx=60, sticky="nsew")

    def _setup_display_frame(self):
        self.display_frame = self._create_frame(row=2)
        self.inner_frame = self._create_inner_frame(self.display_frame)
        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )

    def _add_home_button(self):
        btn = self._create_stylised_button(
            parent=self,title="🛖 Home",
            subtitle="Return to home screen",
            func=self._on_home
        )
        btn.grid(
            row=3, column=0,
            columnspan=2, padx=self.FRAME_PADDING * 10,
            pady=(30, 0), sticky="ew"
        )
        return btn


if __name__ == "__main__":
    from gui.root import Root
    root = Root()
    search_screen = SearchScreen(root)
    search_screen.pack(fill="both", expand=True)
    root.mainloop()
