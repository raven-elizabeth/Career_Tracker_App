from tkinter import Frame, Label
from tkinter.font import nametofont


class Screen(Frame):
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
        self._make_responsive()
        self.heading_font, self.subheading_font, self.italic_font = self._setup_fonts()

    def _make_responsive(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top padding
        self.grid_rowconfigure(1, weight=2)  # First content row
        self.grid_rowconfigure(2, weight=1)  # Middle padding
        self.grid_rowconfigure(3, weight=2)  # Second content row
        self.grid_rowconfigure(4, weight=1)  # Bottom padding

    def _setup_fonts(self):
        heading_font = nametofont("TkHeadingFont").copy()
        heading_font.config(size=self.HEADING_SIZE, weight="bold")

        subheading_font = nametofont("TkHeadingFont").copy()
        subheading_font.config(size=self.SUBHEADING_SIZE)

        italic_font = nametofont("TkTextFont").copy()
        italic_font.config(size=self.BODY_SIZE, slant="italic")

        return heading_font, subheading_font, italic_font

    def _create_frame(self, row):
        frame = Frame(
            self, relief="solid",
            borderwidth=self.BORDER_WIDTH, bg=self.SECONDARY_COLOR
        )
        frame.grid(
            row=row, column=0, columnspan=2,
            padx=self.FRAME_PADDING, pady=10, sticky="nsew"
        )
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame

    def _create_inner_frame(self, parent):
        frame = Frame(parent, bg="white", relief="solid", borderwidth=self.BORDER_WIDTH)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)  # Top spacer
        frame.grid_rowconfigure(2, weight=1)  # Bottom spacer
        return frame

    @staticmethod
    def _create_label(parent, row, text, font, bg, pad_y):
        label = Label(parent, text=text, font=font, bg=bg)
        label.grid(row=row, padx=10, pady=pad_y)
        return label

    @staticmethod
    def _create_simple_separator(parent, row):
        separator = Frame(parent, height=2, bg="black")
        separator.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")
