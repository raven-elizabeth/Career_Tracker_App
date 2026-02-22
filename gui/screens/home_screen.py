from tkinter import Frame, Label
from tkinter.font import nametofont
from gui.root import Root


class HomeScreen(Frame):
    def __init__(self, *args, **kwargs):
        # Colours have been checked for accessibility using WebAIM's contrast checker and are all above 4.5:1 ratio for normal text
        self.primary_color = "#0C2340"
        self.secondary_color = "#A8D5E2"
        self.tertiary_color = "#1D5A87"

        super().__init__(*args, bg=self.primary_color, **kwargs)

        # Make app responsive by configuring grid weights to encourage resizing
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)  # Top padding
        self.grid_rowconfigure(1, weight=2)  # Header frame
        self.grid_rowconfigure(2, weight=1)  # Middle padding
        self.grid_rowconfigure(3, weight=2)  # Options frame
        self.grid_rowconfigure(4, weight=1)  # Bottom padding

        self.heading_font, self.subheading_font, self.italic_font = self._setup_fonts()

        # Copilot suggested using separate frames to make it easier to create a border for multiple widgets
        # This also allows sections to be isolated and styled together
        self.row = 1 # Start at row 1 to leave top padding
        self._create_header_frame()
        self._create_options_frame()


    @staticmethod
    def _setup_fonts():
        heading_font = nametofont("TkHeadingFont").copy()
        heading_font.config(size=30, weight="bold")

        sub_heading_font = nametofont("TkHeadingFont").copy()
        sub_heading_font.config(size=14)

        italic_font = nametofont("TkTextFont").copy()
        italic_font.config(size=12, slant="italic")

        return heading_font, sub_heading_font, italic_font

    def _create_header_frame(self):
        self.header_frame = Frame(self, relief="solid", borderwidth=3, bg=self.secondary_color)
        self.header_frame.grid(row=self.row, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.header_frame.grid_rowconfigure(5, weight=1)  # Bottom padding

        frame_row = 1
        self.icon = Label(self.header_frame, text="📖", font=self.heading_font, bg=self.secondary_color)
        self.icon.grid(row=frame_row, column=0, columnspan=2, padx=10, pady=(10, 0))
        frame_row += 1

        self.header = Label(self.header_frame, text="Career Tracker App", font=self.heading_font, bg=self.secondary_color)
        self.header.grid(row=frame_row, column=0, columnspan=2, padx=10, pady=(0, 5))
        frame_row += 1

        self.welcome_msg = Label(self.header_frame, text="WELCOME TO YOUR PERSONAL TRACKER APP", font=self.subheading_font, bg=self.secondary_color)
        self.welcome_msg.grid(row=frame_row, column=0, columnspan=2, padx=10)
        frame_row += 1

        self.description = Label(self.header_frame, text="Document your work & track your career progress", font=self.italic_font, bg=self.secondary_color)
        self.description.grid(row=frame_row, column=0, padx=10, pady=(0, 20))

        self.row += 2 # Skip a row after header for middle padding

    def _create_options_frame(self):
        self.options_frame = Frame(self, relief="solid", borderwidth=3, bg=self.secondary_color)
        self.options_frame.grid(row=self.row, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)  # Top padding
        self.options_frame.grid_rowconfigure(5, weight=1)  # Bottom padding

        frame_row = 1
        self.options_label = Label(self.options_frame, text="What would you like to do?", font=self.subheading_font, bg=self.secondary_color)
        self.options_label.grid(row=frame_row, column=0, padx=10, pady=(10, 0), sticky="w")
        frame_row += 1

        self._create_simple_separator(self.options_frame, frame_row)
        frame_row += 1

        self.new_entry_btn = self._create_button(
            self.options_frame,
            title="➕ New Entry",
            subtitle="Create a new daily entry"
        )
        self.new_entry_btn.grid(row=frame_row, column=0, padx=20, pady=(0, 10), sticky="nsew")
        frame_row += 1

        self.search_entries_btn = self._create_button(
            self.options_frame,
            title="🔍 Browse Entries",
            subtitle="Search all daily entries"
        )
        self.search_entries_btn.grid(row=frame_row, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.row += 1

    def _create_button(self, parent, title, subtitle):
        btn_frame = Frame(parent, relief="solid", borderwidth=1, cursor="hand2", bg=self.tertiary_color)
        btn_frame.grid_columnconfigure(0, weight=1)

        title_label = Label(btn_frame, text=title, font=self.subheading_font, fg="white", anchor="w", bg=self.tertiary_color)
        title_label.grid(row=0, column=0, padx=10, pady=(8, 0), sticky="ew")

        subtitle_label = Label(btn_frame, text=subtitle, font=self.italic_font, fg="white", anchor="w", bg=self.tertiary_color)
        subtitle_label.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")

        return btn_frame

    def _create_simple_separator(self, parent, row):
        self.separator_frame = Frame(parent, height=2, bg="black")
        self.separator_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")


if __name__ == "__main__":
    root = Root()
    home_screen = HomeScreen(root)
    home_screen.pack(fill="both", expand=True)
    root.mainloop()
