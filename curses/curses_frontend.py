#!/usr/bin/env python3
from fifteen import FifteenPuzzle, Direction
from pathlib import Path

import time
import os
import curses

DEFAULT_HIGHSCORE = 999
SAVE_LOCATION = Path.home()/".15scores"

class CursesApp():
    KEYS_UP    = [ord('w'),ord('W'),ord('j'),ord('J'),curses.KEY_UP]
    KEYS_DOWN  = [ord('s'),ord('S'),ord('k'),ord('K'),curses.KEY_DOWN]
    KEYS_LEFT  = [ord('a'),ord('A'),ord('h'),ord('H'),curses.KEY_LEFT]
    KEYS_RIGHT = [ord('d'),ord('D'),ord('l'),ord('L'),curses.KEY_RIGHT]
    def __init__(self):
        pass
    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(False)
        
        self.puzzle_win  = curses.newwin(4,5,0,0) # extra space for newlines
        self.score_win   = curses.newwin(1,curses.COLS - 1,4,0)
        self.message_win = curses.newwin(1,curses.COLS - 1,5,0)

        self.stdscr.refresh()

        self.score_win.addstr(0,0,"Moves: ")
        self.score_win.refresh()
        
        return self
    def __exit__(self,typ,val,tb):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.curs_set(True)
        curses.echo()
        curses.endwin()
    def draw_puzzle(self,puzzle):
        self.puzzle_win.clear()
        self.puzzle_win.addstr(0,0,str(puzzle))
        self.puzzle_win.refresh()
    def draw_message(self,s):
        self.message_win.clear()
        self.message_win.addstr(0,0,s)
        self.message_win.refresh()
    def draw_score(self,score):
        self.score_win.addstr(0,7,"    ") # clear regular score
        self.score_win.addstr(0,7,str(score))            
        self.score_win.refresh()
    def draw_highscore(self,score):
        self.score_win.addstr(0,11,"High Score:    ")
        self.score_win.addstr(0,23,str(score))
        self.score_win.refresh()

def gethighscore():
    try:
        with open(SAVE_LOCATION, 'r') as f:
            return int(f.readline().rstrip())
    except FileNotFoundError:
        return DEFAULT_HIGHSCORE
    except ValueError:
        os.remove(str(SAVE_LOCATION))
        return DEFAULT_HIGHSCORE+1
 
def sethighscore(s):
    with open(SAVE_LOCATION, 'w') as f:
        f.write(str(s))
          
def main(app):
    puzzle = FifteenPuzzle()
    highscore = gethighscore()

    while True:
        puzzle.shuffle()
        score = 0
        app.draw_score(0)
        if highscore < DEFAULT_HIGHSCORE:
            app.draw_highscore(highscore)
        if highscore == DEFAULT_HIGHSCORE+1:
            app.draw_message("High score file corrupted. Erasing")
            time.sleep(1)
        while not puzzle.is_win():
            app.draw_puzzle(puzzle)
            app.draw_message("arrows/hjkl/wasd:Move|q:quit")

            c = app.stdscr.getch()

            direction = None
            if c in app.KEYS_UP:
                direction = Direction.UP
            if c in app.KEYS_DOWN:
                direction = Direction.DOWN
            if c in app.KEYS_LEFT:
                direction = Direction.LEFT
            if c in app.KEYS_RIGHT:
                direction = Direction.RIGHT
            if direction:
                if puzzle.move(direction):
                    score+=1
                    app.draw_score(score)
                else:
                    app.draw_message("Invalid move")
                    time.sleep(0.5)

            if c in (ord('q'),ord('Q')):
                app.draw_message("Press q again to quit")
                if app.stdscr.getch() in (ord('q'),ord('Q')):
                    return
        app.draw_puzzle(puzzle)     
        while True:
            if score < highscore:
                highscore = score
                app.draw_highscore(score)
                app.draw_message("New high score!")
                sethighscore(score)
                time.sleep(0.5)
            app.draw_message("Play again? (y/n)")
            c = app.stdscr.getch()
            if c in (ord('y'),ord('Y')):
                break # from inner loop to return to outer loop
            if c in (ord('n'),ord('N')):
                return # from entire function
                

if(__name__ == "__main__"):
    with CursesApp() as app:
        main(app)
        print("Thanks for playing!")