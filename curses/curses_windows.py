import curses
import time

def main(stdscr):


    left_menu_win = curses.newwin(10, 10, 1, 1)
    right_menu_win = curses.newwin(10, 10, 1, 40)
    left_menu_win.addstr("testing")
    right_menu_win.addstr("ok")
    # stdscr.addstr("hello world")
    stdscr.refresh()
    right_menu_win.refresh()
    left_menu_win.refresh()

    stdscr.getch()

curses.wrapper(main)