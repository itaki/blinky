

import curses, time

def main(stdscr):
    """checking for keypress"""
    stdscr.clear()
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()

while True:
    key = curses.wrapper(main)
    if key != -1: #
        print(f'key: {key}' ) # prints: 'key: 97' for 'a' pressed
                                        # '-1' on no presses
    #dhtime.sleep(.1)