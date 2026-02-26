from tkinter import Tk


class Root(Tk):
    MIN_WIDTH = 360
    MIN_HEIGHT = 640
    APP_NAME = "Career Tracker App"

    def __init__(self):
        super().__init__()
        # Get user's screen dimensions and set the window to fill the screen on start
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)
        self.title(self.APP_NAME)
