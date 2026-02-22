from tkinter import Tk


class Root(Tk):
    # Colours checked for accessibility using WebAIM contrast checker - all above 4.5:1 ratio
    PRIMARY_COLOR = "#0C2340"
    SECONDARY_COLOR = "#A8D5E2"
    TERTIARY_COLOR = "#1D5A87"

    HEADING_SIZE = 30
    SUBHEADING_SIZE = 14
    BODY_SIZE = 12

    FRAME_PADDING = 20
    BORDER_WIDTH = 3

    def __init__(self):
        super().__init__()

        start_width = 600
        min_width = 500
        start_height = 700
        min_height = 500

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title("Career Tracker App")


if __name__ == "__main__":
    root = Root()
    root.mainloop()
