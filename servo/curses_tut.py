import curses
import time

import curses
import blinky_bits as bb

dict_to_sort = bb.get_tools('tools.json')

def print_menu(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxys()
    num_of_items = len(dict)
    for idx, row in dict_to_sort:
        x = w // 2 - len(row)//2
        y = h // 2 - len(dict_to_sort) // 2 + idx
        stdscr.addstr(y, x, row)
    
    stdscr.refresh()

def main(stdscr):
    print_menu(stdscr)

    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP:
            stdscr.addstr(0,0,"you pressed up")
        elif key == curses.KEY_DOWN:
            stdscr.addstr(0,0,"you pressed down")
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(0,0,"you pressed enter")

        stdscr.refresh()

curses.wrapper(main)