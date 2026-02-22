from tkinter import Frame
from tkinter.font import nametofont

from gui.root import Root


class Screen(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=Root.PRIMARY_COLOR, **kwargs)
        self._make_responsive()
        self.heading_font, self.subheading_font, self.italic_font = self._setup_fonts()

    def _make_responsive(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Top spacer
        self.grid_rowconfigure(1, weight=2)  # First content row
        self.grid_rowconfigure(2, weight=1)  # Middle spacer
        self.grid_rowconfigure(3, weight=2)  # Second content row
        self.grid_rowconfigure(4, weight=1)  # Bottom spacer

    @staticmethod
    def _setup_fonts():
        heading_font = nametofont("TkHeadingFont").copy()
        heading_font.config(size=Root.HEADING_SIZE, weight="bold")

        subheading_font = nametofont("TkHeadingFont").copy()
        subheading_font.config(size=Root.SUBHEADING_SIZE)

        italic_font = nametofont("TkTextFont").copy()
        italic_font.config(size=Root.BODY_SIZE, slant="italic")

        return heading_font, subheading_font, italic_font