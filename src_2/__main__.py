import os

from .model import Sudoku
from .view import SudokuView
from .control import Control

model = Sudoku()
model.set_board(os.path.join(
    os.path.dirname(__file__), "puzzles/sudoku_1.txt"))

view = SudokuView()
# model.execute(1, 1, 1)

# model.change_edit_state()
# model.execute(1, 2, 1)

# view.print_board(model)

control = Control(model, view)

control.main_loop()
