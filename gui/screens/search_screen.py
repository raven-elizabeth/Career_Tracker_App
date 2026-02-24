import datetime
from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    WRAP_LAYOUT_WIDTH = 1000
    INNER_PADDING = 20

    def __init__(self, *args, on_valid_date=None, on_home, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_valid_date = on_valid_date
        self._on_home = on_home
        self._wrap_layout = False

        self._configure_adjacent_grid()
        self._add_back_button()
        self._setup_calendar()
        self._setup_display_frame()

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """Switch between adjacent and wrap layouts based on window width."""
        if event.widget != self:
            return

        should_wrap = event.width < self.WRAP_LAYOUT_WIDTH

        if should_wrap and not self._wrap_layout:
            self._apply_wrap_layout()
            self._wrap_layout = True
        elif not should_wrap and self._wrap_layout:
            self._apply_adjacent_layout()
            self._wrap_layout = False

    def _configure_adjacent_grid(self):
        """Two equal columns; calendar and display frame share the main row."""
        self._configure_responsive_grid(
            col_dict={0: 1, 1: 1},
            row_dict={0: 0, 1: 1, 2: 10, 3: 1}
        )

    def _configure_wrap_grid(self):
        """Single column; calendar and display frame stack vertically."""
        self._configure_responsive_grid(
            col_dict={0: 1, 1: 1},
            row_dict={0: 0, 1: 1, 2: 0, 3: 10, 4: 1}
        )

    def _position_calendar(self, row, colspan):
        """Grid the calendar with consistent padding."""
        pad_x = (self.OUTER_PADDING, self.INNER_PADDING) if colspan == 1 else self.INNER_PADDING
        pad_y = (self.OUTER_PADDING, self.INNER_PADDING) if colspan == 2 else self.OUTER_PADDING
        self.calendar.grid(
            row=row, column=0, columnspan=colspan,
            padx=pad_x, pady=pad_y, sticky="nsew"
        )

    def _setup_calendar(self):
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self._position_calendar(row=2, colspan=1)

    def _setup_display_frame(self):
        self.display_frame = self._create_frame(row=2, column=1, colspan=1)
        self._position_frame(
            self.display_frame, row=2, column=1, colspan=1,
            pad_x=(self.INNER_PADDING, self.OUTER_PADDING)
        )
        self.inner_frame = self._create_inner_frame(self.display_frame)
        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )

    def _apply_adjacent_layout(self):
        self._configure_adjacent_grid()
        self._position_calendar(row=2, colspan=1)
        self._position_frame(
            self.display_frame, row=2, column=1, colspan=1,
            pad_x=(self.INNER_PADDING, self.OUTER_PADDING)
        )

    def _apply_wrap_layout(self):
        self._configure_wrap_grid()
        self._position_calendar(row=2, colspan=2)
        self._position_frame(
            self.display_frame, row=3, column=0,
            pad_x=self.INNER_PADDING,
            pad_y=(self.INNER_PADDING, self.OUTER_PADDING)
        )

    def _add_back_button(self):
        button = self._create_stylised_button(
            parent=self,
            title="⬅️ Back",
            subtitle="Return to home screen",
            func=self._on_home
        )
        self._position_button(button, row=0, colspan=2, pad_y=(20, 10), sticky="w")
        return button
