# Curses theme build
import curses

def get_styles():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    HEADING = curses.color_pair(1)
    WARNING = curses.color_pair(2)
    STATUS = curses.color_pair(3)
    return(HEADING, WARNING, STATUS)

def main():
    styles = get_styles
    

if __name__ == "__main__":
    main()