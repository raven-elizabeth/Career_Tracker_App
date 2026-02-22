from gui.screens.screen import Screen


class HomeScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        column_weights = {0: 1, 1: 1}
        # Row weights set to create more space for header and options frames
        # Includes padding rows at top, middle, and bottom
        row_weights = {0: 1, 1: 2, 2: 1, 3: 2, 4: 1}
        self._make_responsive(column_weights, row_weights)

        self._create_header_frame()
        self._create_options_frame()

    def _create_header_frame(self):
        self.header_frame = self._create_frame(row=1)
        self.header_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.header_frame.grid_rowconfigure(5, weight=1)  # Bottom padding
        frame_row = 1

        self.icon = self._create_label(
            self.header_frame, frame_row, "📖",
            self.heading_font, self.SECONDARY_COLOR, 10
        )
        frame_row += 1

        self.header = self._create_label(
            self.header_frame, frame_row, "Career Tracker App",
            self.heading_font, self.SECONDARY_COLOR, (0, 10)
        )
        frame_row += 1

        self.welcome_msg = self._create_label(
            self.header_frame, frame_row, "WELCOME TO YOUR PERSONAL TRACKER APP",
            self.subheading_font, self.SECONDARY_COLOR, (0, 10)
        )
        frame_row += 1

        self.description = self._create_label(
            self.header_frame, frame_row,
            "Document your work & track your career progress",
            self.italic_font, self.SECONDARY_COLOR, (0, 20)
        )

    def _create_options_frame(self):
        self.options_frame = self._create_frame(row=3)
        self.options_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.options_frame.grid_rowconfigure(5, weight=1)  # Bottom padding
        frame_row = 1

        self.options_label = self._create_label(
            self.options_frame, frame_row, "What would you like to do?",
            self.subheading_font, self.SECONDARY_COLOR, (10, 0)
        )
        frame_row += 1

        self._create_simple_separator(self.options_frame, frame_row)
        frame_row += 1

        self.new_entry_btn = self._create_button(
            self.options_frame, frame_row,
            title="➕ New Entry", subtitle="Create a new daily entry"
        )
        frame_row += 1

        self.search_entries_btn = self._create_button(
            self.options_frame, frame_row,
            title="🔍 Browse Entries", subtitle="Search all daily entries"
        )

    def _create_button(self, parent, row, title, subtitle):
        """Create and grid a stylised button at the given row."""
        btn = self._create_stylised_button(parent, title=title, subtitle=subtitle)
        btn.grid(row=row, column=0, padx=self.FRAME_PADDING, pady=(0, 10), sticky="ew")
        return btn


if __name__ == "__main__":
    from gui.root import Root
    root = Root()
    home_screen = HomeScreen(root)
    home_screen.pack(fill="both", expand=True)
    root.mainloop()
