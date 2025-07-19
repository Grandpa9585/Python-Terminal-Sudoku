from .model import Sudoku, EditingProtectedValueError
from .view import SudokuView


class Control:
    def __init__(self, model: Sudoku, view: SudokuView) -> None:
        self._model: Sudoku = model
        self._view: SudokuView = view

    def main_loop(self) -> None:
        while self._model.is_in_play:
            self._view.clear_screen()
            self._view.print_board(self._model)
            try:
                output: tuple[int, int, int] | None = self._view.get_input()
            except ValueError:
                continue

            if output is None:
                self._model.change_edit_state()
                continue
            else:
                # cop-out solution but oh well
                # reframes the board in cartesian coordinates
                (y, x, value) = output

                x = 9 - x
                y = y - 1

                if not 0 <= x <= 8 or not 0 <= y <= 8 or not 1 <= value <= 9:
                    breakpoint()
                    continue

                try:
                    self._model.execute(x, y, value)
                except EditingProtectedValueError:
                    continue
                # breakpoint()
