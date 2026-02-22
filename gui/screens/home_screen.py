from tkinter import Frame, Label
from tkinter.font import nametofont
from gui.root import Root


class HomeScreen(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=Root.PRIMARY_COLOR, **kwargs)

        # Make app responsive by configuring grid weights to encourage resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top padding
        self.grid_rowconfigure(1, weight=2)  # Header frame
        self.grid_rowconfigure(2, weight=1)  # Middle padding
        self.grid_rowconfigure(3, weight=2)  # Options frame
        self.grid_rowconfigure(4, weight=1)  # Bottom spacer

        self.heading_font, self.subheading_font, self.italic_font = self._setup_fonts()

        # Copilot suggested using multiple frames to separate sections and manage layout more easily
        self._create_header_frame()
        self._create_options_frame()

    @staticmethod
    def _setup_fonts():
        heading_font = nametofont("TkHeadingFont").copy()
        heading_font.config(size=Root.HEADING_SIZE, weight="bold")

        subheading_font = nametofont("TkHeadingFont").copy()
        subheading_font.config(size=Root.SUBHEADING_SIZE)

        italic_font = nametofont("TkTextFont").copy()
        italic_font.config(size=Root.BODY_SIZE, slant="italic")

        return heading_font, subheading_font, italic_font

    def _create_frame(self, row):
        frame = Frame(self, relief="solid", borderwidth=Root.BORDER_WIDTH, bg=Root.SECONDARY_COLOR)
        frame.grid(row=row, column=0, columnspan=2, padx=Root.FRAME_PADDING, pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)  # Top padding
        frame.grid_rowconfigure(5, weight=1)  # Bottom padding
        return frame

    @staticmethod
    def _create_label(parent, row, text, font, pad_y):
        label = Label(parent, text=text, font=font, bg=Root.SECONDARY_COLOR)
        label.grid(row=row, padx=10, pady=pad_y)
        return label

    def _create_header_frame(self):
        self.header_frame = self._create_frame(row=1)
        frame_row = 1

        self.icon = self._create_label(self.header_frame, frame_row, "📖", self.heading_font, 10)
        frame_row += 1

        self.header = self._create_label(self.header_frame, frame_row, "Career Tracker App", self.heading_font, (0, 10))
        frame_row += 1

        self.welcome_msg = self._create_label(
            self.header_frame, frame_row, "WELCOME TO YOUR PERSONAL TRACKER APP",
            self.subheading_font, (0, 10)
        )
        frame_row += 1

        self.description = self._create_label(
            self.header_frame, frame_row,
            "Document your work & track your career progress",
            self.italic_font, (0, 20)
        )

    def _create_options_frame(self):
        self.options_frame = self._create_frame(row=3)
        frame_row = 1

        self.options_label = self._create_label(
            self.options_frame, frame_row, "What would you like to do?",
            self.subheading_font, (10, 0)
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
        btn_frame = Frame(parent, relief="solid", borderwidth=1, cursor="hand2", bg=Root.TERTIARY_COLOR)
        btn_frame.grid_columnconfigure(0, weight=1)

        title_label = Label(
            btn_frame, text=title, font=self.subheading_font,
            fg="white", anchor="w", bg=Root.TERTIARY_COLOR
        )
        title_label.grid(row=0, column=0, padx=10, pady=(8, 0), sticky="ew")

        subtitle_label = Label(
            btn_frame, text=subtitle, font=self.italic_font,
            fg="white", anchor="w", bg=Root.TERTIARY_COLOR
        )
        subtitle_label.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")

        btn_frame.grid(row=row, column=0, padx=Root.FRAME_PADDING, pady=(0, 10), sticky="ew")
        return btn_frame

    @staticmethod
    def _create_simple_separator(parent, row):
        separator = Frame(parent, height=2, bg="black")
        separator.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")


if __name__ == "__main__":
    root = Root()
    home_screen = HomeScreen(root)
    home_screen.pack(fill="both", expand=True)
    root.mainloop()
