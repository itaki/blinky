import curses
import sys

from adafruit_servokit import ServoKit


# Create single-ended input on channel 0
kit = ServoKit(channels=16)

keyboard_present = True



def gate_setter(stdscr):
    """checking for keypress"""
    key = 0
    adjustment = 0
    angle = 90 #set the servo in the middle

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed

    while (key != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()


        if key == curses.KEY_DOWN:
            adjustment = -1
        if key == curses.KEY_LEFT:
            adjustment = -10
        if key == curses.KEY_UP:
            adjustment = 1
        if key == curses.KEY_RIGHT:
            adjustment = 10
        if key == ord('0'):
            angle = 89
            adjustment = 1
        if adjustment != 0:
            angle = angle + adjustment     
            if angle > 180:
                print("TOO HIGH!!!!!!  - Max is 180")
                angle = 180
            if angle < 0: 
                print("TOO LOW!!!!!  - Min is 0")
                angle = 0
            
            print(f"Angle = {angle}")
            kit.servo[0].angle = angle

        # Declaration of strings
        title = "Set Gates"[:width-1]
        subtitle = "Use arrow keys"[:width-1]
        keystr = "Last key pressed: {}".format(key)[:width-1]
        statusbarstr = f"Press 'q' to exit | STATUS BAR | Pos: {angle}"
        if key == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)


        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        key = stdscr.getch()








def main():
    curses.wrapper(gate_setter)

if __name__ == "__main__":
    main()
