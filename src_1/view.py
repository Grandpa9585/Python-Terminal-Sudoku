# from .model import SudokuModel, Cell,
from typing import List, Set

import os

from .model import Instruction


class SudokuView:
    def __init__(self) -> None:
        # three subgrids, three subsubgrids, 8 divisions
        self._subgrid_numbers: str = os.path.join(
            os.path.dirname(__file__), 'numbers/')
        self._BOARD_SIDE_LEN: int = 35
        self._subsubgrid_dividers: Set[int] = {
            3, 7, 15, 19, 27, 31
        }
        self._subgrid_dividers: Set[int] = {11, 23}
        self._print_board: List[List[str]] = [
            ['.' for _ in range(self._BOARD_SIDE_LEN)] for _ in range(self._BOARD_SIDE_LEN)
        ]
        for i in range(self._BOARD_SIDE_LEN):
            for k in self._subsubgrid_dividers:
                self._print_board[i][k] = ' '

            if i in self._subsubgrid_dividers:
                for j in range(self._BOARD_SIDE_LEN):
                    self._print_board[i][j] = ' '

            for k in self._subgrid_dividers:
                self._print_board[i][k] = ' | '

            if i in self._subgrid_dividers:
                for j in range(self._BOARD_SIDE_LEN):
                    self._print_board[i][j] = '-|-' if j in self._subgrid_dividers else '-'

    def print_board(self) -> None:
        for i in range(self._BOARD_SIDE_LEN):
            print(''.join(self._print_board[i]))

    def get_instruction(self) -> Instruction:
        while True:
            uinp = input("instruction: ").lower()
            if uinp in {"add draft", "add guess"}:
                return Instruction.ADD_GUESS
            elif uinp in {"rm draft", "rm guess"}:
                return Instruction.REMOVE_GUESS
            elif uinp in {"add answer"}:
                return Instruction.ADD_ANSWER
            elif uinp in {"rm answer"}:
                return Instruction.REMOVE_ANSWER
            else:
                continue

    def get_value_location(self) -> tuple[int, int, int]:
        (i, j, value) = (0, 0, 0)
        while True:
            try:
                (i, j, value) = (int(c) for c in input(
                    "i j value. Note that (0,0) is top left ").split(' '))
            except ValueError:
                continue

            if 1 <= i <= 9 and 1 <= j <= 9 and 1 <= value <= 9:
                break

        return (i, j, value)

    def set_subgrid_number(self, x: int, y: int, value: int):
        x_reference: int = (x * 3 + x) + x // 9
        y_reference: int = (y * 3 + y) + y // 9
        temp: List[str] = []
        with open(os.path.join(self._subgrid_numbers, f"{str(value)}.txt")) as f:
            temp = f.readlines()
        f.close()

        for i in range(3):
            for j in range(3):
                self._print_board[x_reference + i][y_reference + j] \
                    = temp[i][j]
