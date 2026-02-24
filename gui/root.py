from tkinter import Tk


class Root(Tk):
    START_WIDTH = 1280
    START_HEIGHT = 800
    MIN_WIDTH = 585
    MIN_HEIGHT = 800

    def __init__(self):
        super().__init__()
        self.geometry(f"{self.START_WIDTH}x{self.START_HEIGHT}")
        self.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)
        self.title("Career Tracker App")


if __name__ == "__main__":
    root = Root()
    root.mainloop()
