import os

from copy import deepcopy
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Set

type Board = List[List[Cell]]


@dataclass
class Cell:
    value: int | None
    guesses: Set[int] | None
    is_protected: bool


class CurrentEdit(Enum):
    VALUE = auto()
    DRAFTS = auto()


class EditingProtectedValueError(Exception):
    pass


class Sudoku:
    def __init__(self, is_check_collision: bool = False, is_hold_hand: bool = False) -> None:
        self._board: Board = [
            [Cell(None, None, False) for _ in range(9)] for _ in range(9)
        ]
        self._answer_state = CurrentEdit.VALUE
        self._is_check_collision: bool = is_check_collision
        self._is_hold_hand: bool = is_hold_hand
        self._free_spaces: int = 81
        self._is_in_play: bool = True

    def set_board(self, sudoku_board_location: str) -> None:
        with open(sudoku_board_location) as f:
            temp: List[str] = f.readlines()

        for i in range(9):
            for j in range(9):
                if temp[i][j] != '.':
                    self._board[i][j].value = int(temp[i][j])
                    self._board[i][j].is_protected = True
                    self._free_spaces -= 1
                else:
                    continue

    def get_cell_at(self, x: int, y: int) -> Cell:
        return Cell(self._board[x][y].value, deepcopy(self._board[x][y].guesses), self._board[x][y].is_protected)

    def change_edit_state(self) -> None:
        match self._answer_state:
            case CurrentEdit.VALUE:
                self._answer_state = CurrentEdit.DRAFTS
            case CurrentEdit.DRAFTS:
                self._answer_state = CurrentEdit.VALUE

    def execute(self, x: int, y: int, value: int) -> None:
        cell: Cell = self._board[x][y]

        if cell.is_protected:
            raise EditingProtectedValueError

        if not (1 <= value <= 9):
            raise ValueError

        match self._answer_state:
            case CurrentEdit.VALUE:
                if cell.guesses:
                    cell.guesses = None

                if cell.value == value:
                    cell.value = None
                    self._free_spaces += 1
                else:
                    cell.value = value
                    self._free_spaces -= 1
            case CurrentEdit.DRAFTS:
                if cell.value is not None:
                    self._free_spaces += 1
                    cell.value = None

                if cell.guesses is None:
                    cell.guesses = set()

                if value in cell.guesses:
                    cell.guesses.remove(value)
                else:
                    cell.guesses.add(value)

    @property
    def answer_state(self) -> CurrentEdit:
        return self._answer_state

    @property
    def free_spaces(self) -> int:
        return self._free_spaces

    @property
    def is_in_play(self) -> int:
        return self._is_in_play


model = Sudoku()
model.set_board(os.path.join(
    os.path.dirname(__file__), "puzzles/sudoku_1.txt"))
