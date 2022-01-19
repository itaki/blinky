import curses
import blinky_bits as bb
from adafruit_servokit import ServoKit



def set_angles(self, stdscr, gate_key, side):

        """ CURSES function so nees wrapping, create interface to adjust the gate"""

        my_gate = self.gates[gate_key]
        pin = my_gate.pin
        key = None
        kit = ServoKit(channels=16)
        # adjustment = 0

        too_high = False
        too_low = False
        
        current_min = my_gate.min
        current_max = my_gate.max
        if side == 'min':
            angle = current_min
        else:
            angle = current_max

        rows_of_info = 8
        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Add no echo
        curses.noecho()
        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Initialization
        height, width = stdscr.getmaxyx()
        start_y = int((height // 2) - (rows_of_info // 2 ))
        cent_x = int (width // 2)

        # Loop where k is the last character pressed

        while True:
            
            # Set the adjustment for each key pressed
            if key == "KEY_DOWN":
                adjustment = -1
            elif key == "KEY_LEFT":
                adjustment = -10
            elif key == "KEY_UP":
                adjustment = 1
            elif key == "KEY_RIGHT":
                adjustment = 10
            elif key == "q":
                return -1
            elif key == "s":
                return int(angle)
            elif key == None:
                flagged = True
            if adjustment != 0 or flagged == True:
                flagged = False
                angle = angle + adjustment   
                adjustment = 0  
                if angle > 180:
                    too_high = True
                    angle = 180
                elif angle < 0: 
                    too_low = True
                    angle = 0
                else:
                    too_high = False
                    too_low = False
                
                print(f"Angle = {angle}")
                kit.servo[pin].angle = angle

            # Declaration of strings
            title = f"Set {side} for gate {my_gate.name} at {my_gate.location} on pin {my_gate.pin}"[:width-1]
            instructions = "Use arrow keys  :  '0' to recenter  :  'q' to quit  :  's' to save"[:width-1]
            angle_reading = f"Angle: {angle}"[:width-1]
            if too_low:
                angle_reading = angle_reading + 'WARNING!!! TOO LOW'
            if too_high:
                angle_reading = angle_reading + 'WARNING!!! TOO HIGH'
            statusbarstr = f"Press 'q' to exit | Press 'return' to commit | STATUS BAR | Last key pressed: {format(key)[:width-1]}"

            # Centering calculations
            start_x_title = bb.center_x(width, title)
            start_x_instructions = bb.center_x(width, instructions)
            start_x_angle_reading = bb.center_x(width, angle_reading)
            min_marker = cent_x + (my_gate.min - 90)
            max_marker = cent_x + (my_gate.max - 90)
            angle_marker = cent_x + (angle - 90)

            # Clear the screen
            stdscr.clear()

            # Render status bar
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(height-1, 0, statusbarstr)
            stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            stdscr.attroff(curses.color_pair(3))

            # Render the title
            stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD )
            # Render the instructions
            stdscr.addstr(start_y + 2, start_x_instructions, instructions)
            
            # Render the min marker 
            if side == 'min':
                min_color = curses.color_pair(2)
                max_color = curses.color_pair(1)
            else:
                min_color = curses.color_pair(1)
                max_color = curses.color_pair(2)

            stdscr.addstr(start_y + 3, min_marker, '|', min_color | curses.A_BOLD)
            # Render the max marker 
            stdscr.addstr(start_y + 3, max_marker, '|', max_color | curses.A_BOLD)
            # Render the current angle marker gauge
            stdscr.addstr(start_y + 3, angle_marker, '|')
            # Render the angle gauge
            stdscr.addstr(start_y + 4, (width // 2) - 90, '-' * 180)
            stdscr.addstr(start_y + 5, cent_x - 91, '0', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x - 61, '30', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x - 31, '60', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x - 1, '90', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x + 29, '120', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x + 59, '150', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x + 89, '180', curses.color_pair(1))
            # Render the current values
            stdscr.addstr(start_y + 7, start_x_angle_reading, angle_reading)



            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            key = stdscr.getkey()