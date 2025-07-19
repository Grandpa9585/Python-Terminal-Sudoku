from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Set, Tuple

import os

type Row = List[Cell]
type Board = List[Row]
type Cell_String = Tuple[Tuple[str, str, str,],
                         Tuple[str, str, str,],
                         Tuple[str, str, str,],]


@dataclass
class Cell:
    value: int | None
    guesses: List[int]
    is_protected: bool


class AnswerStatus(Enum):
    VALID_ANSWER = auto()
    INVALID_ANSWER = auto()
    START = auto()
    GAME_OVER = auto()


class Instruction(Enum):
    ADD_ANSWER = auto()
    REMOVE_ANSWER = auto()
    ADD_GUESS = auto()
    REMOVE_GUESS = auto()
    CANCEL_GUESS = auto()


class SudokuSolver:
    def __init__(self, board: Board) -> None:
        self._board: Board = board

    def solve(self) -> None:
        self._solve(0, 0)

    def _solve(self, x: int, y: int) -> bool:
        if (x, y) == (9, 0):
            return True

        if self._board[x][y].value is not None:
            return self._solve(x + 1 if y == 8 else x, 0 if y == 8 else y + 1)

        for guess in range(9):
            if self._is_valid(x, y, guess):
                self._board[x][y].value = guess
            else:
                continue

            if self._solve(x + 1 if y == 8 else x, 0 if y == 8 else y + 1):
                return True
            else:
                self._board[x][y].value = None

        return False

    def _is_valid(self, x: int, y: int, guess: int) -> bool:
        for i in range(9):
            if self._board[i][y].value == guess:
                return False

        for i in range(9):
            if self._board[x][i].value == guess:
                return False

        x_start: int = (x // 3) * 3
        y_start: int = (y // 3) * 3

        for i in range(x_start, x_start + 3):
            for j in range(y_start, y_start + 3):
                if self._board[i][j].value == guess:
                    return False
        return True


class ChangingProtectedValue(Exception):
    pass


class SudokuTextToCell:
    def __init__(self, puzzle_name: str) -> None:
        script_dir: str = os.path.dirname(__file__)
        puzzle: str = 'puzzles/' + puzzle_name
        self._path: str = os.path.join(script_dir, puzzle)
        self.board: Board = [
            [Cell(None, [], False) for _ in range(9)] for _ in range(9)
        ]
        self._NUMBERS = '123456789'

    def convert(self) -> None:
        with open(self._path, 'r') as f:
            temp: List[str] = f.readlines()
        f.close()

        for i in range(9):
            for j in range(9):
                if temp[i][j] in self._NUMBERS:
                    self.board[i][j].value = int(temp[i][j])
                    self.board[i][j].is_protected = True


class SudokuModel:
    def __init__(self, board: Board, is_check_guess: bool = False, is_check_guess_with_solved_board: bool = False) -> None:
        self._board: Board = board
        self._solved_board: Board = []
        if is_check_guess_with_solved_board:
            self._solved_board = deepcopy(board)
            solver = SudokuSolver(self._solved_board)
            solver.solve()
        self._check_with_solved_board: bool = is_check_guess_with_solved_board
        self._check_guess: bool = is_check_guess

        self._answer_status: AnswerStatus = AnswerStatus.START
        self._collisions: Set[Tuple[int, int]] = set()

    def run_instruction(self, instruction: Instruction, x: int, y: int, value: int) -> None:
        match instruction:
            case Instruction.ADD_ANSWER:
                if not self._board[x][y].is_protected:
                    self._board[x][y].value = value
                    self._board[x][y].guesses.clear()
                else:
                    raise ChangingProtectedValue
            case Instruction.REMOVE_ANSWER:
                if not self._board[x][y].is_protected:
                    self._board[x][y].value = None
                else:
                    raise ChangingProtectedValue
            case Instruction.ADD_GUESS:
                if value in self._board[x][y].guesses:
                    return None
                self._board[x][y].value = None
                self._board[x][y].guesses.append(value)
            case Instruction.REMOVE_GUESS:
                if value not in self._board[x][y].guesses:
                    return None
                for i in range(len(self._board[x][y].guesses)):
                    if self._board[x][y].guesses[i] == value:
                        self._board[x][y].guesses.pop(i)
            case Instruction.CANCEL_GUESS:
                return None

        self._check_against_solved(x, y, value)
        self._check_regular_collision(x, y, value)

    def _check_regular_collision(self, x: int, y: int, value: int) -> None:
        if not self._check_guess:
            return None

        for i in range(9):
            if self._board[i][y].value == value:
                self._collisions.add((x, y))
                self._answer_status = AnswerStatus.INVALID_ANSWER
                return None

        for i in range(9):
            if self._board[x][i].value == value:
                self._answer_status = AnswerStatus.INVALID_ANSWER
                self._collisions.add((x, y))
                return None

        x_start: int = (x // 3) * 3
        y_start: int = (y // 3) * 3

        for i in range(x_start, x_start + 3):
            for j in range(y_start, y_start + 3):
                if self._board[i][j].value == value:
                    self._answer_status = AnswerStatus.INVALID_ANSWER
                    self._collisions.add((x, y))
                    return None

        self._answer_status = AnswerStatus.VALID_ANSWER

    def _check_against_solved(self, x: int, y: int, value: int) -> None:
        if not self._check_with_solved_board:
            return None

        if self._board[x][y].value == self._solved_board[x][y].value:
            self._answer_status = AnswerStatus.VALID_ANSWER
        else:
            self._answer_status = AnswerStatus.INVALID_ANSWER

    @property
    def board(self) -> Board:
        return deepcopy(self._board)
