import tkinter as tk

from . import config


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Had"
        self.pixels_per_block = config.UI_PIXELS_PER_BLOCK

    def _create_board_display(self, board: list[list[any]]):
        pass