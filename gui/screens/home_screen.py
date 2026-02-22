from tkinter import Frame, Label
from tkinter.font import nametofont
from gui.root import Root


class HomeScreen(Frame):
    # Colours checked for accessibility using WebAIM contrast checker - all above 4.5:1 ratio
    PRIMARY_COLOR = "#0C2340"
    SECONDARY_COLOR = "#A8D5E2"
    TERTIARY_COLOR = "#1D5A87"

    HEADING_SIZE = 30
    SUBHEADING_SIZE = 14
    BODY_SIZE = 12

    FRAME_PADDING = 20
    BORDER_WIDTH = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=self.PRIMARY_COLOR, **kwargs)

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
        heading_font.config(size=HomeScreen.HEADING_SIZE, weight="bold")

        subheading_font = nametofont("TkHeadingFont").copy()
        subheading_font.config(size=HomeScreen.SUBHEADING_SIZE)

        italic_font = nametofont("TkTextFont").copy()
        italic_font.config(size=HomeScreen.BODY_SIZE, slant="italic")

        return heading_font, subheading_font, italic_font

    def _create_header_frame(self):
        self.header_frame = Frame(self, relief="solid", borderwidth=self.BORDER_WIDTH, bg=self.SECONDARY_COLOR)
        self.header_frame.grid(row=1, column=0, columnspan=2, padx=self.FRAME_PADDING, pady=10, sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.header_frame.grid_rowconfigure(5, weight=1)  # Bottom padding

        frame_row = 1
        self.icon = Label(self.header_frame, text="📖", font=self.heading_font, bg=self.SECONDARY_COLOR)
        self.icon.grid(row=frame_row, column=0, padx=10, pady=(10, 0))
        frame_row += 1

        self.header = Label(
            self.header_frame, text="Career Tracker App",
            font=self.heading_font, bg=self.SECONDARY_COLOR
        )
        self.header.grid(row=frame_row, column=0, padx=10, pady=(0, 5))
        frame_row += 1

        self.welcome_msg = Label(
            self.header_frame, text="WELCOME TO YOUR PERSONAL TRACKER APP",
            font=self.subheading_font, bg=self.SECONDARY_COLOR
        )
        self.welcome_msg.grid(row=frame_row, column=0, padx=10)
        frame_row += 1

        self.description = Label(
            self.header_frame, text="Document your work & track your career progress",
            font=self.italic_font, bg=self.SECONDARY_COLOR
        )
        self.description.grid(row=frame_row, column=0, padx=10, pady=(0, 20))

    def _create_options_frame(self):
        self.options_frame = Frame(self, relief="solid", borderwidth=self.BORDER_WIDTH, bg=self.SECONDARY_COLOR)
        self.options_frame.grid(row=3, column=0, columnspan=2, padx=self.FRAME_PADDING, pady=(0, 10), sticky="nsew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.options_frame.grid_rowconfigure(5, weight=1)  # Bottom padding

        frame_row = 1
        self.options_label = Label(
            self.options_frame, text="What would you like to do?",
            font=self.subheading_font, bg=self.SECONDARY_COLOR
        )
        self.options_label.grid(row=frame_row, column=0, padx=10, pady=(10, 0), sticky="w")
        frame_row += 1

        self._create_simple_separator(self.options_frame, frame_row)
        frame_row += 1

        self.new_entry_btn = self._create_button(
            self.options_frame,
            title="➕ New Entry",
            subtitle="Create a new daily entry"
        )
        self.new_entry_btn.grid(row=frame_row, column=0, padx=self.FRAME_PADDING, pady=(0, 10), sticky="ew")
        frame_row += 1

        self.search_entries_btn = self._create_button(
            self.options_frame,
            title="🔍 Browse Entries",
            subtitle="Search all daily entries"
        )
        self.search_entries_btn.grid(row=frame_row, column=0, padx=self.FRAME_PADDING, pady=(0, 10), sticky="ew")

    def _create_button(self, parent, title, subtitle):
        btn_frame = Frame(parent, relief="solid", borderwidth=1, cursor="hand2", bg=self.TERTIARY_COLOR)
        btn_frame.grid_columnconfigure(0, weight=1)

        title_label = Label(
            btn_frame, text=title, font=self.subheading_font,
            fg="white", anchor="w", bg=self.TERTIARY_COLOR
        )
        title_label.grid(row=0, column=0, padx=10, pady=(8, 0), sticky="ew")

        subtitle_label = Label(
            btn_frame, text=subtitle, font=self.italic_font,
            fg="white", anchor="w", bg=self.TERTIARY_COLOR
        )
        subtitle_label.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")

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
