# This screen is the first thing users see when they open the app.
# It provides a welcoming message and clear options to either create a new entry or browse existing entries.

from gui.screens.screen import Screen


class HomeScreen(Screen):
    def __init__(self, *args, on_new_entry, on_search, **kwargs):
        super().__init__(*args, **kwargs)

        self._on_new_entry = on_new_entry
        self._on_search = on_search

        self._configure_grid()
        self._create_header_frame()
        self._create_options_frame()

    def _configure_grid(self):
        """Set row and column weights. Padding rows at top, middle, and bottom."""
        self._configure_responsive_grid(
            column_weights={0: 1, 1: 1},
            row_weights={0: 1, 1: 4, 2: 1, 3: 4, 4: 1}
        )

    def _create_header_frame(self):
        """Create the header frame with icon, main heading, welcome message, and description labels."""
        self.header_frame = self._create_frame()
        self.header_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.header_frame.grid_rowconfigure(5, weight=1)  # Bottom padding
        frame_row = 1

        self.icon = self._create_label(
            self.header_frame, frame_row, "📖",
            self.heading_font, self.SECONDARY_COLOR, pad_y=10
        )
        frame_row += 1

        self.header = self._create_label(
            self.header_frame, frame_row, "Career Tracker App",
            self.heading_font, self.SECONDARY_COLOR, pad_y=(0, 10)
        )
        frame_row += 1

        self.welcome_msg = self._create_label(
            self.header_frame, frame_row, "WELCOME TO YOUR PERSONAL TRACKER APP",
            self.subheading_font, self.SECONDARY_COLOR, pad_y=(0, 10)
        )
        frame_row += 1

        self.description = self._create_label(
            self.header_frame, frame_row,
            "Document your work & track your career progress",
            self.italic_font, self.SECONDARY_COLOR, pad_y=(0, 20)
        )

    def _create_options_frame(self):
        """Create options frame with subheading and buttons for creating a new entry or browsing existing entries."""
        self.options_frame = self._create_frame(row=3)
        self.options_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.options_frame.grid_rowconfigure(5, weight=1)  # Bottom padding
        frame_row = 1

        self.options_label = self._create_label(
            self.options_frame, frame_row, "What would you like to do?",
            self.subheading_font, self.SECONDARY_COLOR,
            pad_y=(10, 0), pad_x=self.OUTER_PADDING, anchor="w"
        )
        frame_row += 1

        self._create_separator(self.options_frame, frame_row, pad_x=self.OUTER_PADDING)
        frame_row += 1

        self.new_entry_btn = self._add_button(
            title="➕ New Entry",
            subtitle="Create a new daily entry",
            func=self._on_new_entry,
            row=frame_row
        )
        frame_row += 1

        self.search_entries_btn = self._add_button(
            title="🔍 Browse Entries",
            subtitle="Search all daily entries",
            func=self._on_search,
            row=frame_row
        )

    def _add_button(self, title, subtitle, func, row):
        """Create and grid a stylised option button inside the options frame."""
        btn = self._create_stylised_button(
            parent=self.options_frame,
            title=title,
            subtitle=subtitle,
            func=func
        )
        self._position_button(btn, row=row, colspan=1)
        return btn
