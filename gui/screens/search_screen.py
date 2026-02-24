import datetime
from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    WRAP_LAYOUT_WIDTH = 1000

    def __init__(self, *args, on_valid_date=None, on_home, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_valid_date = on_valid_date
        self._on_home = on_home

        self._configure_grid()
        self.wrap_layout = False

        self._add_back_button()
        self._setup_calendar()
        self._setup_display_frame()

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        # Only respond to events on outer frame (SearchScreen)
        if event.widget != self:
            return

        is_wrap_layout_width = event.width < self.WRAP_LAYOUT_WIDTH

        if is_wrap_layout_width and not self.wrap_layout:
            self._apply_wrap_layout()
            self.wrap_layout = True
        elif not is_wrap_layout_width and self.wrap_layout:
            self._apply_adjacent_layout()
            self.wrap_layout = False

    def _configure_grid(self):
        column_weights = {0: 1, 1: 1}
        # Row weights set; display frame and calendar have more weight to take up more space.
        row_weights = {0: 0, 1: 1, 2: 10, 3: 1}
        self._configure_responsive_grid(column_weights, row_weights)

    def _setup_calendar(self):
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self.calendar.grid(row=2, column=0, columnspan=1, padx=(self.FRAME_PADDING, 10), pady=20, sticky="nsew")

    def _apply_adjacent_layout(self):
        self._configure_grid()
        self.calendar.grid(row=2, column=0, columnspan=1, padx=(self.FRAME_PADDING, 10), pady=20, sticky="nsew")
        self._position_frame(self.display_frame, row=2, column=1, colspan=1)

    def _apply_wrap_layout(self):
        self._configure_responsive_grid({0: 1, 1: 1}, {0: 0, 1: 1, 2: 0, 3: 10, 4: 1})
        self.calendar.grid(row=2, column=0, columnspan=2, padx=60, pady=20, sticky="nsew")
        self._position_frame(self.display_frame, row=3, column=0)

    def _setup_display_frame(self):
        self.display_frame = self._create_frame(row=2, column=1, colspan=1)
        self.inner_frame = self._create_inner_frame(self.display_frame)
        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )

    def _add_back_button(self):
        btn = self._create_stylised_button(
            parent=self,title="⬅️ Back",
            subtitle="Return to home screen",
            func=self._on_home
        )
        btn.grid(
            row=0, column=0, padx=self.FRAME_PADDING,
            pady=40, sticky="w"
        )
        return btn
