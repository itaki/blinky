from enum import Enum
from collections import namedtuple

import random

Coordinates = namedtuple("Coords",["x","y"])
Direction = Enum("Direction","UP DOWN LEFT RIGHT")

class FifteenPuzzle:
    initial_board = (("1","2","3","4"),
                     ("5","6","7","8"),
                     ("9","A","B","C"),
                     ("D","E","F"," "))
    def __init__(self):
        self.board = [list(row) for row in self.initial_board] # tuple to list
        self.shuffle()
    def shuffle(self):
        for _ in range(100):
            self.move(random.choice(list(Direction)))
    def findzero(self):
        for y,row in enumerate(self.board):
            for x,v in enumerate(row):
                if v == " ":
                    return Coordinates(x,y)
    def move(self,direction):
        p = self.findzero()
        if direction == Direction.UP:
            if p.y == 3: return False
            self.board[p.y][p.x]   = self.board[p.y+1][p.x]
            self.board[p.y+1][p.x] = " "
        if direction == Direction.DOWN:
            if p.y == 0: return False
            self.board[p.y][p.x]   = self.board[p.y-1][p.x]
            self.board[p.y-1][p.x] = " "
        if direction == Direction.LEFT:
            if p.x == 3: return False
            self.board[p.y][p.x]   = self.board[p.y][p.x+1]
            self.board[p.y][p.x+1] = " "
        if direction == Direction.RIGHT:
            if p.x == 0: return False
            self.board[p.y][p.x]   = self.board[p.y][p.x-1]
            self.board[p.y][p.x-1] = " "
        return True
    def is_win(self):
        return tuple(tuple(row) for row in self.board) == self.initial_board
    def __str__(self):
        ret = ""
        for row in self.board:
            for val in row:
                ret += val
            ret += "\n"
        return ret[:-1]             # strip trailing newline
