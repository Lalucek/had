from __future__ import annotations

from enum import Enum

import config
import random


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def opposite_direction(self) -> Direction:
        x, y = self.value
        return Direction((-x, -y))


class Player:
    def __init__(self, x_pos: int, y_pos: int, direction: Direction):
        self.x, self.y, self.direction = x_pos, y_pos, direction
        self.lenght = 0

    def change_direction(self, new_direction: Direction) -> None:
        if self.lenght > 1:
            if new_direction != self.direction.opposite_direction():
                self.direction = new_direction
            return
        self.direction = new_direction


class Food:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x, self.pos_y = pos_x, pos_y


class Game:
    def __init__(self):
        self.board_size = config.BOARD_SIZE
        self.player = Player(config.START_POSITION, config.START_POSITION)
        self.food_pieces = []

    def _spawn_new_food(self):
        x = random.randint(0, self.board_size - 1)
        y = random.randint(0, self.board_size - 1)
        self.food_pieces.append(Food(x, y))
