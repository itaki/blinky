import curses
import time
from tkinter import N
import blinky_bits as bb
file = 'tools.json'

#cur_list = ['TableSaw', 'mitersaw', 'bandsaw']
arrows = '----- MOVING ❱❱❱❱❱'
bulk_copy = 'Move Remaining --❱❱'
save_status = 'Compete to save'
options_list = [arrows, '', bulk_copy, save_status, 'Quit - Discard' ]


window_widths = 30
num_of_options = 5

def get_list(file):
    cur_dict = bb.get_tools()
    cur_list = list(cur_dict.keys())
    return cur_list



# create windows for each seletion
def build_cur_win(stdscr, cur_list):
    '''Builds window to the left of the screen for current list. Returns cur_win'''
    h, w = stdscr.getmaxyx()
    center_x = int( w // 2 ) 
    height = len(cur_list) 
    y_placement = (int( h // 2 ) - ( height // 2 )) - 1 # Place window just below center
    x_placement = int(center_x - window_widths - (window_widths // 2))
    cur_win = curses.newwin(height, window_widths, y_placement, x_placement ) # height, width, begin_y, begin_x
    return cur_win

def build_new_win(stdscr, cur_list):
    '''Builds window to the right of the screen for current list. Returns new_win'''
    h, w = stdscr.getmaxyx()
    center_x = int( w // 2 ) 
    height = len(cur_list) 
    y_placement = (int( h // 2 ) - ( height // 2 )) - 1 # Place window just below center
    x_placement = int(center_x + (window_widths // 2))
    new_win = curses.newwin(height, window_widths, y_placement, x_placement ) # height, width, begin_y, begin_x
    return new_win

def build_options_win(stdscr):
    '''Builds a window in the middle of the screen that holds a few options. Returns options_win'''
    h, w = stdscr.getmaxyx()
    center_x = int( w // 2 ) 
    height = num_of_options
    y_placement = int(( h // 2) - ( height // 2)) - 1
    x_placement = int( center_x - window_widths // 2)
    options_win = curses.newwin( height, window_widths, y_placement, x_placement )
    return options_win

def print_cur_list(cur_win, cur_list, idx, state):
    ''' Prints the current list'''
    cur_win.clear()
    h, w = cur_win.getmaxyx()
    for i, row in enumerate(cur_list):
        x = w//2 - len(row)//2
        y = h//2 - len(cur_list)//2 + i
        if i == idx and state == 'left':
            cur_win.attron(curses.color_pair(1))
            cur_win.addstr(y, x, row)
            cur_win.attroff(curses.color_pair(1))
        else:
            cur_win.addstr(y, x, row)
    cur_win.refresh()

def print_new_list(new_win, new_list, idx, state):
    new_win.clear()
    h, w = new_win.getmaxyx()
    for i, row in enumerate(new_list):
        x = w//2 - len(row)//2
        y = h//2 - len(new_list)//2 + i
        if i == idx and state == 'right':
            new_win.attron(curses.color_pair(1))
            new_win.addstr(y, x, row)
            new_win.attroff(curses.color_pair(1))
        else:
            new_win.addstr(y, x, row)
    new_win.refresh()

def print_options(options_win, options_list, cur_list, idx, state):
    options_win.clear()
    h, w = options_win.getmaxyx()

    # Show options current state
    if state == 'left':
        arrows = '----- MOVING ❱❱❱❱❱'
        color_pair = curses.color_pair(4)
    elif state == 'right':
        arrows = '❰❰❰❰❰ MOVING -----'
        color_pair = curses.color_pair(3)
    elif state == 'options':
        arrows = '▼     OPTIONS     ▼'
        color_pair = curses.color_pair(5)
    options_win.addstr(0, w // 2 - len(arrows) // 2, arrows, color_pair )

    # Determin which move string to use
    if len(cur_list) != 0:
        move_str = 'Move Remaining --❱❱'
    else:
        move_str = '❰❰ -- Reset List'
    
    # Determine how to display it
    if idx == 2 and state == 'options':
        options_win.attron(curses.color_pair(1))
        options_win.addstr(2, w // 2 - len(move_str) // 2, move_str )
        options_win.attroff(curses.color_pair(1))
    else:
        options_win.addstr(2, w // 2 - len(move_str) // 2, move_str )
    

    # Show Save
    save_str = 'Save New Order'
    if len(cur_list) == 0:
        if idx == 3 and state == 'options':
            options_win.attron(curses.color_pair(1))
            options_win.addstr(3,  w // 2 - len(save_str) //2, save_str)
            options_win.attroff(curses.color_pair(1))
        else:
            options_win.addstr(3,  w // 2 - len(save_str) //2, save_str)
        
    else:
        options_win.attron(curses.A_DIM)
        if idx == 3 and state == 'options':
            options_win.attron(curses.color_pair(1))
            options_win.addstr(3,  w // 2 - len(save_str) //2, save_str)
            options_win.attroff(curses.color_pair(1))
        else:
            options_win.addstr(3,  w // 2 - len(save_str) //2, save_str)
        options_win.attroff(curses.A_DIM)
    
    

            
    # Show quit
    quit_str = 'Quit - Discard'
    if idx == 4 and state == 'options':
        options_win.attron(curses.color_pair(1))
        options_win.addstr(4,  w // 2 - len(save_str) //2, quit_str)
        options_win.attroff(curses.color_pair(1))
    else:
        options_win.addstr(4,  w // 2 - len(save_str) //2, quit_str)

    options_win.refresh()


def order_list(stdscr, original_list):
    cur_list = original_list
    new_list = []
    curses.curs_set(0) #sets the cursor to invisible
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    # Set the windows. This can probably be done in a function
    #cur_win = curses.newwin(10, 10, 10, 1) # height, width, begin_y, begin_x
    cur_win = build_cur_win(stdscr, cur_list)
    new_win = build_new_win(stdscr, cur_list)
    options_win = build_options_win(stdscr)

    idx = 0
    state = 'left'
    h, w = stdscr.getmaxyx()

    # Print Heading
    heading = '   CURRENT ORDER          -         OPTIONS          -          NEW ORDER   '
    y_pos = (h // 2) - (len(cur_list) // 2) - 3
    x_pos = (w // 2) - (len(heading) // 2)
    stdscr.addstr(y_pos, x_pos, heading, curses.color_pair(2))

    stdscr.refresh()
    print_cur_list(cur_win, cur_list, idx, state)
    print_options(options_win, options_list, cur_list, idx, state)
    print_new_list(new_win, new_list, idx, state)


    while True:
        key = stdscr.getch()
        if state == 'left':


            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(cur_list)-1:
                idx += 1
            elif key == curses.KEY_RIGHT:
                state = 'options'
                idx = 2
            elif key == curses.KEY_ENTER or key in [10, 13]:
                new_list.append(cur_list[idx])
                cur_list.remove(cur_list[idx])
                if len(cur_list) == 0:
                    state = 'options'
                    idx = 3
                elif idx > (len(cur_list)-1):
                    idx = len(cur_list)-1


        elif state == 'right':
            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(new_list)-1:
                idx += 1
            elif key == curses.KEY_LEFT:
                state = 'options'
                idx = 2
            elif key == curses.KEY_ENTER or key in [10, 13]:
                cur_list.append(new_list[idx])
                new_list.remove(new_list[idx])
                if len(new_list) == 0:
                    state = 'options'
                    idx = 2
                elif idx > (len(new_list) - 1):
                    idx = len(new_list) - 1
        
        elif state == 'options':
            # then start the real app
            if key == curses.KEY_UP and idx > 2:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(options_list)-1:
                idx += 1
            elif key == curses.KEY_LEFT and len(cur_list) != 0:
                state = 'left'
                idx = 0
            elif key == curses.KEY_RIGHT and len(new_list) != 0:
                state = 'right'
                idx = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if idx == 2: # do the move thing
                    if len(cur_list) == 0: # restarting from scratch THIS IS BROKEN
                        cur_list = original_list
                        new_list = []
                        state = 'left'
                        idx = 0 
                    else: # just moving the rest of the items
                        for i, val in enumerate(cur_list):
                            new_list.append(val)
                        cur_list = []
                if idx == 3 and len(cur_list) == 0: # alls good. Let's save
                    return new_list 
                if idx == 4:
                    return original_list


        print_cur_list(cur_win, cur_list, idx, state)
        print_options(options_win, options_list, cur_list, idx, state)
        print_new_list(new_win, new_list, idx, state)

def reorder(cur_dict):
    cur_list = list(cur_dict.keys())
    original_list = cur_list
    new_list = curses.wrapper(order_list, original_list)
    new_dict = {}
    for i, r in enumerate(new_list):
        new_dict[r] = cur_dict[r]
    return new_dict
def main():
    original_list = list(get_list(file))
    new_list = curses.wrapper(order_list, original_list)
    print('SUCCESS!!!')
    print(new_list)

if __name__ == '__main__':
    main()

