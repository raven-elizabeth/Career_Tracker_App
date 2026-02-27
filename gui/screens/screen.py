# This module defines the Screen class, which serves as a base for all GUI screens in the application.
# It provides common styling, layout configuration, and utility methods.
# Note: This class should not be instantiated directly.
# Currently, not all methods are reused by more than one screen,
# but they have potential for reuse as the application grows.

from tkinter import Frame, Label, messagebox
from tkinter.font import nametofont


class Screen(Frame):
    # Colours checked for accessibility using WebAIM contrast checker - all above 4.5:1 ratio
    # Values stored here to align with DRY principle (Don't Repeat Yourself) for easy updates & consistency
    PRIMARY_COLOR = "#0C2340"
    SECONDARY_COLOR = "#A8D5E2"
    TERTIARY_COLOR = "#1D5A87"
    INNER_FRAME_COLOR = "white"

    HEADING_SIZE = 30
    SUBHEADING_SIZE = 14
    BODY_SIZE = 12

    OUTER_PADDING = 60
    BORDER_WIDTH = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=self.PRIMARY_COLOR, **kwargs)
        self._setup_fonts()

    def _setup_fonts(self):
        """Create and configure font styles for headings, subheadings, and italic text using Tkinter's named fonts."""

        self.heading_font = nametofont("TkHeadingFont").copy()
        self.heading_font.config(size=self.HEADING_SIZE, weight="bold")

        self.subheading_font = nametofont("TkHeadingFont").copy()
        self.subheading_font.config(size=self.SUBHEADING_SIZE)

        self.italic_font = nametofont("TkTextFont").copy()
        self.italic_font.config(size=self.BODY_SIZE, slant="italic")

    def _configure_responsive_grid(self, column_weights, row_weights):
        """Set column and row weights to make the screen responsive to resizing."""

        for col, weight in column_weights.items():
            self.grid_columnconfigure(col, weight=weight)
        for row, weight in row_weights.items():
            self.grid_rowconfigure(row, weight=weight)

    def _create_frame(self, row=1, column=0, colspan=2):
        """Create a reusable frame with consistent styling and secondary colour."""

        frame = Frame(
            self, relief="solid",
            borderwidth=self.BORDER_WIDTH, bg=self.SECONDARY_COLOR
        )
        self._position_frame(frame, row=row, column=column, colspan=colspan)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame

    def _position_frame(self, parent, row, column, colspan=2, pad_x=None, pad_y=None):
        """Grid a frame with consistent padding and stretch behaviour."""

        pad_x = pad_x if pad_x is not None else self.OUTER_PADDING
        pad_y = pad_y if pad_y is not None else 10
        parent.grid(
            row=row, column=column, columnspan=colspan,
            padx=pad_x, pady=pad_y, sticky="nsew"
        )

    def _position_button(self, btn, row, column=0, colspan=2, pad_x=None, pad_y=(0, 10), sticky="ew"):
        """Grid a stylised button with consistent padding."""

        pad_x = pad_x if pad_x is not None else self.OUTER_PADDING
        btn.grid(
            row=row, column=column, columnspan=colspan,
            padx=pad_x, pady=pad_y, sticky=sticky
        )

    def _create_inner_frame(self, parent):
        """Create an inner frame to make content display clearer against the background"""

        frame = Frame(parent, bg=self.INNER_FRAME_COLOR, relief="solid", borderwidth=self.BORDER_WIDTH)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        return frame

    @staticmethod
    def _create_label(parent, row, text, font, bg, pad_y=0, pad_x=10, anchor="center"):
        """Create a label with consistent styling and padding."""

        label = Label(parent, text=text, font=font, bg=bg, anchor=anchor)
        label.grid(row=row, padx=pad_x, pady=pad_y, sticky="ew" if anchor != "center" else "")
        return label

    @staticmethod
    def _create_separator(parent, row, pad_x=10):
        """Create a simple horizontal separator line."""

        separator = Frame(parent, height=2, bg="black")
        separator.grid(row=row, column=0, padx=pad_x, pady=(0, 10), sticky="ew")

    def _create_stylised_button(self, parent, title, subtitle, func):
        """
        Create a clickable frame styled as a button with a title and subtitle.
        Uses Frame + Labels with .bind() instead of a Button widget, as this
        allows for multi-line content and custom styling not available on Button.
        Each label captures func via a default argument to avoid late-binding issues with looping.
        """

        btn_frame = Frame(parent, relief="solid", borderwidth=1, cursor="hand2", bg=self.TERTIARY_COLOR)
        btn_frame.grid_columnconfigure(0, weight=1)

        title_label = Label(
            btn_frame, text=title, font=self.subheading_font,
            fg="white", anchor="w", bg=self.TERTIARY_COLOR
        )
        title_label.grid(row=0, column=0, padx=10, pady=(8, 0), sticky="ew")
        title_label.bind("<Button-1>", lambda event, f=func: f())

        subtitle_label = Label(
            btn_frame, text=subtitle, font=self.italic_font,
            fg="white", anchor="w", bg=self.TERTIARY_COLOR
        )
        subtitle_label.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")
        subtitle_label.bind("<Button-1>", lambda event, f=func: f())

        btn_frame.bind("<Button-1>", lambda event, f=func: f())
        return btn_frame

    @staticmethod
    def _show_error(title, message):
        """Display an error message in a pop-up window."""
        messagebox.showerror(title=title, message=message)
