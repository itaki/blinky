import curses

def main(screen):
    win1 = curses.newwin(3, 10, 0, 0)
    win2 = curses.newwin(3, 10, 3, 0)
    for count in ['3', '2', '1', 'Go!']:
        win1.addstr(1, 1, 'Win1: ' + count)
        win2.addstr(1, 1, 'Win2: ' + count)

        screen.refresh()
        win1.refresh()
        win2.refresh()
        screen.getch()

curses.wrapper(main)