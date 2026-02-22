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
        self._setup_fonts()

    def _setup_fonts(self):
        self.heading_font = nametofont("TkHeadingFont").copy()
        self.heading_font.config(size=self.HEADING_SIZE, weight="bold")

        self.subheading_font = nametofont("TkHeadingFont").copy()
        self.subheading_font.config(size=self.SUBHEADING_SIZE)

        self.italic_font = nametofont("TkTextFont").copy()
        self.italic_font.config(size=self.BODY_SIZE, slant="italic")

    # Set column and row weights to make the screen responsive to resizing
    def _make_responsive(self, col_dict, row_dict):
        for col, weight in col_dict.items():
            self.grid_columnconfigure(col, weight=weight)
        for row, weight in row_dict.items():
            self.grid_rowconfigure(row, weight=weight)

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

    # Create an inner frame with white background for content display
    def _create_inner_frame(self, parent):
        frame = Frame(parent, bg="white", relief="solid", borderwidth=self.BORDER_WIDTH)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        return frame

    # Create a label with consistent styling and padding
    @staticmethod
    def _create_label(parent, row, text, font, bg, pad_y):
        label = Label(parent, text=text, font=font, bg=bg)
        label.grid(row=row, padx=10, pady=pad_y)
        return label

    # Create a simple horizontal separator line
    @staticmethod
    def _create_simple_separator(parent, row):
        separator = Frame(parent, height=2, bg="black")
        separator.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")

    # Create a button-like frame with title and subtitle labels
    def _create_stylised_button(self, parent, title, subtitle):
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

