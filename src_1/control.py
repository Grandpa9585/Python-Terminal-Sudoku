from .model import SudokuModel, Instruction, ChangingProtectedValue
from .view import SudokuView


class Control:
    def __init__(self, model: SudokuModel, view: SudokuView) -> None:
        self._model = model
        self._view = view

    def main_loop(self) -> None:
        while True:
            self._view.clear_screen()
            self._view.print_board()
            instruction: Instruction = self._view.get_instruction()
            (x, y, value) = self._view.get_value_location()

            if value == 0:
                continue

            try:
                self._model.run_instruction(instruction, x, y, value)
            except ChangingProtectedValue:
                continue

            self._view.instruction_handler(
                self._model, instruction, x, y, value)
