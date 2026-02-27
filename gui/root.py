from tkinter import Tk


class Root(Tk):
    MIN_WIDTH = 360
    MIN_HEIGHT = 640
    APP_NAME = "Career Tracker App"

    def __init__(self):
        super().__init__()
        self.state("zoomed")  # Start maximised at user's screen size
        self.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)
        self.title(self.APP_NAME)
