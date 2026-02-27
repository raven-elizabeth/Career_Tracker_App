# This file contains the Root class, which is the main window of the application.
# It sets the window title, minimum size, and starts maximised to provide a consistent user experience.
# It is passed as the parent to all screens, which are then packed and unpacked to navigate between them.

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
