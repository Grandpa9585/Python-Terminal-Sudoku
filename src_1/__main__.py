import os

from .view import SudokuView
from .model import SudokuTextToCell, SudokuModel
from .control import Control

view = SudokuView()
# view.set_subgrid_number(0, 0, None)
# view.set_subgrid_number(1, 1, 1)
# view.set_subgrid_number(2, 2, 2)
# view.set_subgrid_number(3, 3, 3)
# view.set_subgrid_number(4, 4, 4)
# view.set_subgrid_number(5, 5, 5)
# view.set_subgrid_number(6, 6, 6)
# view.set_subgrid_number(7, 7, 7)
# view.set_subgrid_number(8, 8, 8)

# view.set_subgrid_number(0, 1, 1)
# view.set_subgrid_number(0, 2, 2)
# view.set_subgrid_number(0, 3, 3)
# view.set_subgrid_number(0, 4, 4)
# view.set_subgrid_number(0, 5, 5)
# view.set_subgrid_number(0, 6, 6)
# view.set_subgrid_number(0, 7, 7)
# view.set_subgrid_number(0, 8, 8)

# view.set_subgrid_number(1, 0, 1)
# view.set_subgrid_number(2, 0, 2)
# view.set_subgrid_number(3, 0, 3)
# view.set_subgrid_number(4, 0, 4)
# view.set_subgrid_number(5, 0, 5)
# view.set_subgrid_number(6, 0, 6)
# view.set_subgrid_number(7, 0, 7)
# view.set_subgrid_number(8, 0, 8)

# view.print_board()

model = SudokuTextToCell('sudoku_1.txt')
script_dir = os.path.dirname(__file__)
rel_path = 'puzzles/sudoku_1.txt'
model.convert()


sudoku_model = SudokuModel(model.board)

for i in range(9):
    for j in range(9):
        view.set_subgrid_number(i, j, sudoku_model.board[i][j].value)

control = Control(sudoku_model, view)
control.main_loop()

# view.set_subsubgird_number(0, 2, 1)
# view.set_subsubgird_number(0, 2, 2)
# view.set_subsubgird_number(0, 2, 3)
# view.set_subsubgird_number(0, 2, 4)
# view.set_subsubgird_number(0, 2, 5)
# view.set_subsubgird_number(0, 2, 6)
# view.set_subsubgird_number(0, 2, 7)
# view.set_subsubgird_number(0, 2, 8)
# view.set_subsubgird_number(0, 2, 9)

# view.set_subsubgird_number(3, 5, 1)
# view.set_subsubgird_number(3, 5, 2)
# view.set_subsubgird_number(3, 5, 3)
# view.set_subsubgird_number(3, 5, 4)
# view.set_subsubgird_number(3, 5, 5)
# view.set_subsubgird_number(3, 5, 6)
# view.set_subsubgird_number(3, 5, 7)
# view.set_subsubgird_number(3, 5, 8)
# view.set_subsubgird_number(3, 5, 9)


# view.print_board()
