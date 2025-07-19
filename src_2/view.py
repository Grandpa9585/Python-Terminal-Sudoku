from typing import List, Set, Tuple

import os

from .model import Sudoku, CurrentEdit, Cell


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

    def print_board(self, model: Sudoku) -> None:
        for i in range(9):
            for j in range(9):
                x_reference: int = (i * 3 + i) + i // 9
                y_reference: int = (j * 3 + j) + j // 9

                cell: Cell = model.get_cell_at(i, j)
                if cell.value is None:
                    self._subgrid_edit(x_reference, y_reference, None)
                    if cell.guesses is not None:
                        for value in cell.guesses:
                            self._subsubgrid_edit(
                                x_reference, y_reference, value)
                elif cell.guesses is None:
                    self._subgrid_edit(x_reference, y_reference, cell.value)

        for i in range(self._BOARD_SIDE_LEN):
            print(''.join(self._print_board[i]))

        print("The current edit state is ", end='')
        match model.answer_state:
            case CurrentEdit.VALUE:
                print("full answer")
                pass
            case CurrentEdit.DRAFTS:
                print("drafts")
                pass

    def _subgrid_edit(self, x_ref: int, y_ref: int, value: int | None):
        with open(os.path.join(self._subgrid_numbers, f"{str(value)}.txt")) as f:
            temp = f.readlines()
        f.close()

        for i in range(3):
            for j in range(3):
                self._print_board[x_ref + i][y_ref + j] \
                    = temp[i][j]

    def _subsubgrid_edit(self, x_ref: int, y_ref: int, value: int | None) -> None:
        if value is None:
            self._subgrid_edit(x_ref, y_ref, value)
            return None

        self._print_board[x_ref + (value - 1) //
                          3][y_ref + (value - 1) % 3] = str(value)

    def get_input(self) -> Tuple[int, int, int] | None:
        uinp: str = input("""put in the cartesian coordinate and value separated by spaces (bottom left is 1 1 X)
type 'change' to change the input type: """).lower()

        if uinp == "change":
            return None

        out: Tuple[int, ...] = tuple(int(c) for c in uinp.split())

        if len(out) == 3:
            return out
        else:
            raise ValueError

    def clear_screen(self) -> None:
        os.system("clear")
