import datetime
from tkcalendar import Calendar

from gui.screens.screen import Screen


class SearchScreen(Screen):
    WRAP_LAYOUT_WIDTH = 1000
    INNER_PADDING = 20

    def __init__(self, *args, on_date, on_home, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_date = on_date
        self._on_home = on_home
        self._wrap_layout = False

        self._configure_adjacent_grid()
        self._position_button(
            self._add_back_button(func=self._on_home),
            row=0, colspan=2, pad_y=(20, 10), sticky="w"
        )
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

    def _setup_calendar(self):
        self.calendar = Calendar(self, selectmode="day", maxdate=datetime.date.today())
        self._position_calendar(row=2, colspan=1)
        self.calendar.bind("<<CalendarSelected>>",self._on_date_selected)

    def _on_date_selected(self, event):
        selected_date = self.calendar.get_date()
        date = datetime.datetime.strptime(selected_date, "%m/%d/%y").strftime("%Y-%m-%d")
        entry = self._on_date(date)
        if entry:
            self._on_valid_date(entry)
        else:
            self._reset_widgets()

    def _on_valid_date(self, entry):
        self._reset_widgets(default=False)
        self._display_entry(entry)

    def _display_entry(self, entry):
        for row, (field, value) in enumerate(entry.entry_dict.items()):
            label = self._create_label(
                self.inner_frame, row=row,
                text=f"{field.replace('_', ' ').title()}: {value.capitalize() if value else 'N/A'}",
                font=self.subheading_font, bg="white",
                anchor="w", pad_y=5
            )
            self.inner_frame.bind(
                "<Configure>",
                lambda event, lbl=label: lbl.config(wraplength=event.width - 20),
                add="+"
            )
        self.inner_frame.grid_rowconfigure(len(entry.entry_dict), weight=1)

    def _reset_widgets(self, default=True):
        # Clear screen (destroy widgets, hide default message)
        widgets = self.inner_frame.winfo_children()
        widgets.remove(self.default_msg)
        for widget in widgets:
            widget.destroy()

        # Remove per-entry wraplength bindings added in _display_entry
        self.inner_frame.unbind("<Configure>")

        # Reset the spacer rows used by default message centering
        self.inner_frame.grid_rowconfigure(0, weight=0)
        self.inner_frame.grid_rowconfigure(2, weight=0)
        # Reset the trailing spacer row added after entry labels
        self.inner_frame.grid_rowconfigure(len(self.inner_frame.grid_slaves()), weight=0)

        # Show default message if default=True, otherwise hide it
        if not default:
            self.default_msg.grid_remove()
        else:
            # Restore spacer rows for centered default message
            self.inner_frame.grid_rowconfigure(0, weight=1)
            self.inner_frame.grid_rowconfigure(2, weight=1)
            self.default_msg.grid(row=1, padx=10, pady=10)

    def _position_calendar(self, row, colspan):
        """Grid the calendar with consistent padding."""
        pad_x = (self.OUTER_PADDING, self.INNER_PADDING) if colspan == 1 else self.INNER_PADDING
        pad_y = (self.OUTER_PADDING, self.INNER_PADDING) if colspan == 2 else self.OUTER_PADDING
        self.calendar.grid(
            row=row, column=0, columnspan=colspan,
            padx=pad_x, pady=pad_y, sticky="nsew"
        )

    def _setup_display_frame(self):
        self.display_frame = self._create_frame(row=2, column=1, colspan=1)
        self._position_frame(
            self.display_frame, row=2, column=1, colspan=1,
            pad_x=(self.INNER_PADDING, self.OUTER_PADDING)
        )
        # Prevent outer frame from resizing to fit content from entry data
        self.display_frame.grid_propagate(False)
        self.inner_frame = self._create_inner_frame(self.display_frame)
        # Prevent inner frame from resizing to fit content from entry data
        self.inner_frame.grid_propagate(False)
        self.inner_frame.grid_rowconfigure(0, weight=1)  # Top spacer
        self.inner_frame.grid_rowconfigure(2, weight=1)  # Bottom spacer
        self.default_msg = self._create_label(
            self.inner_frame, row=1, text="Select a date to view your entries...",
            font=self.italic_font, bg="white", pad_y=10
        )
