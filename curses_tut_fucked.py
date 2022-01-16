import curses
import time


import blinky_bits as bb

dict_to_sort = bb.get_tools('tools.json')
item_list = dict_to_sort.keys()
new_list = []



def current_order(current_order_win, current_row_idx, side):
    current_order_win.clear()
    h, w = current_order_win.getmaxyx()
    for idx, row in enumerate(item_list):
        x = w // 3 - len(row)
        y = h // 2 - len(item_list) // 2 + idx
        if idx == current_row_idx:
            current_order_win.attron(curses.color_pair(4))
            current_order_win.addstr(y, x, row)
            current_order_win.attroff(curses.color_pair(4))
        else:

            current_order_win.addstr(y, x, row)
    
    current_order_win.refresh()



def main(stdscr):
    curses.curs_set(0) #sets the cursor to invisible
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)
    h, w = stdscr.getmaxyx()
    center_x = int( w // 2 ) 
    max_height = len(item_list) + 2
    y_placement = int( h // 2 ) - ( max_height // 2 )
    current_order_win = curses.newwin(max_height, 30, y_placement, center_x - 50  )
    # new_order_win = curses.newwin(max_height , 30, y_placement, center_x + 20)
    # tools_win = curses.newwin(10, 30, h//2 - 5, center_x - 15)
    current_order_idx = 0 
    # new_order_idx = 0
    side = 'current'

    while True:
        current_order(current_order_win, current_order_idx, side )
        # new_order(stdscr, new_row_idx, side)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_order_idx > 0:
            current_order_idx -= 1

        elif key == curses.KEY_DOWN and current_order_idx < (len(dict_to_sort) - 1):
            current_order_idx += 1
        
        elif key == curses.KEY_ENTER or key in [10, 13]:
            new_list.append(item_list[current_order_idx])
            item_list.pop[current_order_idx]
        
        # print_menu(stdscr, current_row_idx)

        stdscr.refresh()

curses.wrapper(main)