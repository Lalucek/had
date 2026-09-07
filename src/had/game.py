from __future__ import annotations

import random
from collections import deque
from enum import Enum

from . import config, ui


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
        self.head_x, self.head_y, self.direction = x_pos, y_pos, direction
        self.lenght = 0
        self._body = deque()
        self._body.append((self.head_x, self.head_y))

    def change_direction(self, new_direction: Direction) -> None:
        if self.lenght > 1:
            if new_direction != self.direction.opposite_direction():
                self.direction = new_direction
            return
        self.direction = new_direction

    @property
    def body(self) -> deque:
        return self._body

    def add_body_part(self) -> None:
        self._body.append(self.body[-1])

    def move(self, food: list[tuple[int,int]]) -> tuple[int,int]:
        new_head = self._body[0] + self.direction
        self._body.append(new_head)
        return new_head

    def head_illegal(self, new_head) -> bool:
        return bool(
            new_head in self._body
            or new_head[0] < 0
            or new_head[0] >= config.BOARD_SIZE
            or new_head[1] < 0
            or new_head[1] >= config.BOARD_SIZE
        )

    def head_food_collision(self, new_head: tuple[int,int], food_pieces: list[tuple[int,int]]) -> bool:
        return new_head in food_pieces


class Food:
    def __init__(self, pos_x: int, pos_y: int, color: str | None = None):
        self.pos_x, self.pos_y = pos_x, pos_y
        if color == None:
            self._pick_color()
        elif color not in config.FOOD_COLORS:
            self._color = "#ff5252"
        else:
            self._color = color

    @property
    def color(self):
        return self._color

    @property
    def position(self):
        return (self.pos_x, self.pos_y)

    def _pick_color(self) -> None:
        self._color = config.FOOD_COLORS[random.randint(0, len(config.FOOD_COLORS) - 1)]


class Game:
    def __init__(self):
        self.title("Had")
        self.board_size = config.BOARD_SIZE
        self.player = Player(config.START_POSITION, config.START_POSITION)
        self.food_pieces = []
        self._ui = ui.View()

    def _spawn_new_food(self):
        occupied = {food.position for food in self.food_pieces} | set(self.player.body)
        while (
            new_food_pos := (
                random.randint(0, self.board_size - 1),
                random.randint(0, self.board_size - 1),
            )
        ) in occupied:
            pass
        self.food_pieces.append(Food(*new_food_pos))

    def start_game(self):
        self.game_loop()

    def game_loop(self):
        # Update player position based on current position
        # self._update_player_position() returns False if the move is illegal (game over), True otherwise
        if self._update_player_position():
            self._ui.draw_game(self.board, self.food_pieces, self.player.body)

    def _update_player_position(self) -> bool:
        """Returns False if the move is illegal (game over), True otherwise"""
        self.board[self.player.postion[0]][self.player.position[1]]
        new_head = self.player.move(self.food_pieces)
        if self.player.head_illegal(new_head):
            #Game over
            print("Game over")
            return False
        if not self.player.head_food_collision(new_head, self.food_pieces):
            self.player.body.pop()
        return True