import tkinter as tk
from collections.abc import Iterable
from typing import NamedTuple

import config

"""
Food dependency removed
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Food
"""
class Block(NamedTuple):
    x: int
    y: int
    color: str

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "Had"
        self.pixels_per_block = config.UI_PIXELS_PER_BLOCK
        self.canvas = tk.Canvas(self, width=config.BOARD_SIZE * self.pixels_per_block,
                                 height=config.BOARD_SIZE  * self.pixels_per_block, bg=config.BG_COLOR)
        self.canvas.pack()

    def draw_game(self, blocks: Iterable[Block]):
        self.canvas.delete("all")
        for block in blocks:
            x_topright, y_topright = block.x * self.pixels_per_block, block.y * self.pixels_per_block
            x_botleft, y_botleft = x_topright + self.pixels_per_block, y_topright + self.pixels_per_block
            self.canvas.create_rectangle(x_topright, y_topright, x_botleft, y_botleft, fill=block.color)

    def tick(self):
        self.after(config.MS_PER_FRAME, self.tick)
    
if __name__ == "__main__":
    v = View()
    v.draw_game(None)
    v.mainloop()
    