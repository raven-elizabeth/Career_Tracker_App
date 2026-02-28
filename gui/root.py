"""
This file contains the Root class, which is the main window of the application.
It sets the window title, minimum size, and starts maximised to provide a consistent user experience.
It is passed as the parent to all screens, which are then packed and unpacked to navigate between them.
"""

from tkinter import Tk


class Root(Tk):
    # Minimum sizes chosen to ensure all content fits and is not cut off.
    # Would like to add responsive design in the future for smaller sizes, but constrained by time and scope of project.
    MIN_WIDTH = 1400
    MIN_HEIGHT = 800
    APP_NAME = "Career Tracker App"

    def __init__(self):
        super().__init__()
        self.state("zoomed")  # Start maximised at user's screen size
        self.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)
        self.title(self.APP_NAME)
