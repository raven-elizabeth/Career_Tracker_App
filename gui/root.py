from tkinter import Tk


class Root(Tk):
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
