from tkinter import Frame, Label, Button
from tkinter.font import nametofont
from gui.root import Root


class HomeScreen(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the grid layout responsive by configuring column and row weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1) # Row between header and buttons
        self.grid_rowconfigure(10, weight=1)   # Last row

        self.heading_font, self.subheading_font, self.italic_font = self._setup_fonts()

        # Copilot suggested using separate frames to make it easier to create a border for multiple widgets
        # This also allows sections to be isolated and styled together
        self.row = 0
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
        self.header_frame = Frame(self, relief="solid", borderwidth=3)
        self.header_frame.grid(row=self.row, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)

        self.icon = Label(self.header_frame, text="📖", font=self.heading_font)
        self.icon.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(10, 0))
        self.row += 1

        self.header = Label(self.header_frame, text="Career Tracker App", font=self.heading_font)
        self.header.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(0, 5))
        self.row += 1

        self.welcome_msg = Label(self.header_frame, text="WELCOME TO YOUR PERSONAL TRACKER APP", font=self.subheading_font)
        self.welcome_msg.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(0, 0))
        self.row += 1

        self.description = Label(self.header_frame, text="Document your work & track your career progress",
                                 font=self.italic_font)
        self.description.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(0, 20))
        self.row += 2

    def _create_options_frame(self):
        self.options_frame = Frame(self, relief="solid", borderwidth=3)
        self.options_frame.grid(row=self.row, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)

        self.options_label = Label(self.options_frame, text="What would you like to do?", font=self.subheading_font)
        self.options_label.grid(row=self.row, column=0, padx=10, pady=(10, 0), sticky="w")
        self.row += 1

        self._create_simple_separator(self.options_frame)
        self.row += 1

        self.new_entry_btn = Button(self.options_frame, text="➕ New Entry", font=self.subheading_font, width=15, height=2)
        self.new_entry_btn.grid(row=self.row, column=0, padx=20, pady=0, sticky="nsew")
        self.row += 1

        self.search_entries_btn = Button(self.options_frame, text="🔍 Browse Entries", font=self.subheading_font, width=15, height=2)
        self.search_entries_btn.grid(row=self.row, column=0, padx=20, pady=20, sticky="nsew")
        self.row += 1

    def _create_simple_separator(self, parent):
        self.separator_frame = Frame(parent, height=2, bg="black")
        self.separator_frame.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")


if __name__ == "__main__":
    root = Root()
    home_screen = HomeScreen(root)
    home_screen.pack(fill="both", expand=True)
    root.mainloop()
