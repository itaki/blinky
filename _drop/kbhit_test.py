# import os
# if os.name == 'nt':
#     import msvcrt
# else:
#     import sys, select

# def kbhit():
#     ''' Returns True if a keypress is waiting to be read in stdin, False otherwise.
#     '''
#     if os.name == 'nt':
#         return msvcrt.kbhit()
#     else:
#         dr,dw,de = select.select([sys.stdin], [], [], 0)
#         return dr != []

# while True:
#     print(kbhit())

import curses, time

def main(stdscr):
    """checking for keypress"""
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()

while True:
    key = curses.wrapper(main)
    if key != -1: #
        print(f'key: {key}' ) # prints: 'key: 97' for 'a' pressed
                                        # '-1' on no presses
    #time.sleep(.1)