#!/usr/bin/env python3
#https://codereview.stackexchange.com/questions/237353/15-puzzle-in-python

import curses
from pathlib import Path
from typing import Tuple

from fifteen import FifteenPuzzle, Direction

DEFAULT_HIGHSCORE = 999
SAVE_LOCATION = Path.home() / ".15scores"
DIRECTION_TO_CUSTOM_KEYS = {
    Direction.UP: ("w", "j"),
    Direction.DOWN: ("s", "k"),
    Direction.LEFT: ("a", "h"),
    Direction.RIGHT: ("d", "l"),
}


class Scoreboard:
    score: int
    high_score: int
    save_file: Path

    def __init__(self, save_file: Path) -> None:
        self.save_file = save_file
        self._load_high_score()
        self.score = 0

    def _load_high_score(self) -> None:
        try:
            self.high_score = int(self.save_file.read_text().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = DEFAULT_HIGHSCORE

    def increment(self, k: int = 1) -> None:
        self.score += k

    def reset(self) -> None:
        self.score = 0

    @property
    def current_and_high_score(self) -> Tuple[int, int]:
        return (self.score, self.high_score)

    def publish(self) -> bool:
        if self.score < self.high_score:
            self.save_file.write_text(str(self.score))
            self.high_score = self.score
            return True
        return False


class CursesApp:
    QUIT_KEYS = (ord("q"), ord("Q"))
    YES_KEYS = (ord("y"), ord("Y"))
    NO_KEYS = (ord("n"), ord("N"))
    KEY_TO_DIRECTION = {
        curses.KEY_UP: Direction.UP,
        curses.KEY_DOWN: Direction.DOWN,
        curses.KEY_LEFT: Direction.LEFT,
        curses.KEY_RIGHT: Direction.RIGHT,
    }

    def __init__(self, stdscr, puzzle, scoreboard):
        self.stdscr = stdscr
        self.puzzle = puzzle
        self.scoreboard = scoreboard
        curses.curs_set(False)
        curses.use_default_colors()
        self.puzzle_win = curses.newwin(4, 5, 0, 0)
        self.score_win = curses.newwin(1, curses.COLS - 1, 4, 0)
        self.stdscr.addstr(5, 0, "arrows/hjkl/wasd:move | q:quit")
        self.message_win = curses.newwin(1, curses.COLS - 1, 6, 0)
        self.stdscr.refresh()

        _ord = ord
        key_map = self.KEY_TO_DIRECTION
        for direction, keys in DIRECTION_TO_CUSTOM_KEYS.items():
            for key in keys:
                key_map[_ord(key.lower())] = direction
                key_map[_ord(key.upper())] = direction

    def start(self):
        while self.play():
            self.scoreboard.reset()
            self.puzzle.shuffle()

    def play(self):
        while self.refresh() and not self.puzzle.is_solved:
            c = self.stdscr.getch()
            if c in self.QUIT_KEYS:
                self.draw_message("Press q again to quit")
                if self.stdscr.getch() in self.QUIT_KEYS:
                    return False
                self.clear_message()
            elif direction := self.KEY_TO_DIRECTION.get(c, None):
                if self.puzzle.move(direction):
                    self.scoreboard.increment()

        if self.scoreboard.publish():
            self.draw_scores()
            self.draw_message("New high score!")
            self.block_on_input()

        return self.wants_to_play_again()

    def wants_to_play_again(self):
        while True:
            self.draw_message("Play again? (y/n)")
            c = self.stdscr.getch()
            if c in self.YES_KEYS:
                self.clear_message()
                return True
            elif c in self.NO_KEYS:
                self.clear_message()
                return False

    def draw_scores(self):
        current_score, high_score = self.scoreboard.current_and_high_score
        scores = f"Moves: {current_score} | High Score: {high_score}"
        self.score_win.clear()
        self.score_win.addstr(0, 0, scores)
        self.score_win.refresh()

    def refresh(self):
        self.puzzle_win.addstr(0, 0, str(self.puzzle))
        self.puzzle_win.refresh()
        self.draw_scores()
        return True

    def draw_message(self, s):
        self.message_win.clear()
        self.message_win.addstr(0, 0, s)
        self.message_win.refresh()

    def clear_message(self):
        self.message_win.clear()
        self.message_win.refresh()

    def block_on_input(self):
        return self.stdscr.getch()


def main(stdscr):
    puzzle = FifteenPuzzle()
    scoreboard = Scoreboard(SAVE_LOCATION)
    CursesApp(stdscr, puzzle, scoreboard).start()


if __name__ == "__main__":
    curses.wrapper(main)
    print("Thanks for playing!")