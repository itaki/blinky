# gate manager
import curses
import keyboard # this library requires running the script as root
import time
import os, sys
import json
import questionary as q
import get_full_path
import blinky_bits as bb
import reorder_dict
from pathlib import Path
from adafruit_servokit import ServoKit
from gpiozero import LED, RGBLED, Button


from styles import custom_style_dope, get_styles

style = custom_style_dope

# Initialize the servo board
kit = ServoKit(channels=16)
gates_file = 'gates.json'
backup_dir = '_BU'

class Gate:
    def __init__(self, name, number, location, status, pin, minimum, maximum, info):
        self.name = name
        self.number = number
        self.location = location
        self.status = status
        self.pin = pin
        self.min = minimum
        self.max = maximum
        self.info = info

    def open(self):
        kit.servo[self.pin].angle = self.max
        print(f'opening {self.name}')
        # send maximum to gate
        self.status = 0


    def close(self):
        kit.servo[self.pin].angle = self.min
        print(f'closing {self.name}')
        # send minimum to gate
        self.status = 1

class Gate_Manager:
    gates: dict
    gates_file: str
    changed = False
    backed_up = False

    def __init__(self, gates_file, backup_dir) -> None:
        self.gates_file = gates_file
        self.load_gates()
        self.backup_dir = backup_dir

    def select_gates_file(self):
        files = os.listdir(self.backup_dir)
        files.reverse()
        print (files)
        selected_file = q.select("Which file would you like to restore? Top is newest",
                    choices = files, 
                    default=None, 
                    qmark='?', 
                    pointer='»', 
                    style=style, 
                    use_shortcuts=False, 
                    use_arrow_keys=True, 
                    use_indicator=True, 
                    use_jk_keys=True, 
                    show_selected=True, 
                    instruction=None,).ask()
        selected_file = backup_dir+'/'+selected_file
        return selected_file
    
    def load_gates(self, gates_file = gates_file): 
        '''Takes a JSON file and returns a dictionary of Gate objects'''
        gates_list = []  # list
        gates = {}
            # LOAD ALL THE GATES
        if os.path.exists(gates_file): # if there is a gates file load it
            file_path = get_full_path.path(gates_file)  # set the file path
            with open(file_path, 'r') as f:  # read the gate list
                gates_list = json.load(f)  # load gate list into python

            #print (gates_list)

            for gate in gates_list:
                gates[gate['name']] = Gate(
                    gate['name'],
                    gate['number'],
                    gate['location'],
                    gate['status'],
                    gate['pin'],
                    gate['min'],
                    gate['max'],
                    gate['info']
                )
                # 1print(gate)
        else:
            print('no gate file available') #Fix this in future versions with get_gates
        self.gates = gates
        return(gates)

    def write_gates(self, note = ''):
        '''Writes the gates in memory to the gates_file. Makes a backup beforehand'''
        # Backup current file
        bb.backup_file(self.gates_file, note)
        # create the file path
        file_path = get_full_path.path(self.gates_file)  # set the file path
        #convert the gates object to a format that can be written by json
        new_gates_file = []
        new_gates_list = list(self.gates.values())
        for g in new_gates_list:
            new_gates_file.append(g.__dict__)
        with open(file_path, 'w') as f:  # 'w' writes over the whole file
            f.write(json.dumps(new_gates_file, indent = 4))
            print(f"New gates written to {file_path}")
    
    def view_gates(self):
        if self.gates == False:
            if q.confirm("There are no gates, would you like to load some gates?", style=style).ask:
                self.load_gates()
                return True
        else:
            for gate in self.gates:
                s_gate = self.gates[gate]
                print(s_gate.__dict__)
            return False
    
    def view_gates_compact(self):
        if self.gates == False:
            if q.confirm("There are no gates, would you like to load some gates?", style=style).ask:
                self.load_gates()
                return True
        else:
            for gate in self.gates:
                s_gate = self.gates[gate]
                print (f"Gate {s_gate.name} at {s_gate.location} on pin {s_gate.pin} min:{s_gate.min} | max:{s_gate.max} -- {s_gate.info}")
            return False
                
    def clear_gates(self):
        action = q.confirm(f"ARE YOU SURE YOU WANT TO CLEAR ALL GATES?", style=style).ask()
        
        if action:
            self.gates = {}
            return True
        return False

    def set_gate_name(self, gate_key):
        my_gate = self.gates[gate_key]
        #ask about the current name and renaming it
        print(f"Current name is {my_gate.name}")
        print("Depending on the size of the gate button, the name should be very short. One to 3 charaters.")
        new_name = q.text("What name would you like to use?", style = style).ask()
        if new_name == 'new':
            print("Cannon use 'new' as name, please choose another?")
            self.set_gate_name(gate_key)
        # for all the g's in gates check to see if it's the same name
        for g in self.gates:
            s_gate = self.gates[g] # note that in this case, 'gate' alone is also the name of the key that is paired with the object
            if new_name == g != gate_key:
                print(f"That name alread taken by the gate at loaction {s_gate.location} on pin {s_gate.pin}")
                self.set_gate_name(gate_key)
            #first change the key  
            #https://stackoverflow.com/questions/16475384/rename-a-dictionary-key
            print(f"Saving gate {my_gate.name} as {new_name}")
            new_gates = {new_name if k == my_gate.name else k:v for k,v in self.gates.items() }
            self.gates = new_gates
            #now change the name since we know the key value for it 
            self.gates[new_name].name = new_name
            return True
            
        else:
            return False

    def set_gate_pin(self, gate_key):
        #my_gate = self.gates[gate_key]
        # get requested pin
        requested_pin = int(q.text("What pin is the gate on? (0 - 15)", style = style).ask())
        if 0 <= requested_pin <= 15:
            if len(self.gates) != 0:
                for g in self.gates:
                    s_gate = self.gates[g]
                    if requested_pin == s_gate.pin:
                        print(f"{requested_pin} already used by gate {s_gate.name} at {s_gate.location}. Double check your gates. 'q' to quit.") 
                        self.set_gate_pin(gate_key)
            self.gates[gate_key].pin = int(requested_pin)
            return True
            
        elif requested_pin == 'q':
            return False
        else:
            print(f"{requested_pin} not a pin number. 'q' to quit without setting pin")

    def rattle_gate(self, stdscr, gate_key):
        ''' CURSES function so needs wrapping, takes gate_key, moves gate around until quit'''
        my_gate = self.gates[gate_key]
        # get size of terminal canvas
        height, width = stdscr.getmaxyx()
        styles = get_styles()
        stdscr.clear()
        stdscr.nodelay(True)

        #create the strings
        info = f"Currently identifying GATE {my_gate.name} at {my_gate.location}"
        instructions = "'q' to quit"
        #calculate position
        info_x = bb.center_x(width, info)
        info_y = int((height // 2) - 1)
        instructions_x = bb.center_x(width, instructions)
        instructions_y = int((height // 2) + 1)
        cent_x = int(width // 2)
        cent_y = int(height // 2)
        # print to screen
        stdscr.addstr(info_y, info_x, info, styles['heading'])
        stdscr.addstr(instructions_y, instructions_x, instructions, styles['warning'])
        angle = 70
        increase = True
        key = None
        while True:
            try:
                key = stdscr.getkey()
            except:
                key = None
            if key == None:
                #stdscr.addstr("It's working")
                if increase == True:
                    angle = angle +1
                    kit.servo[my_gate.pin].angle = angle
                    if angle >= 110:
                        increase = False
                else:
                    angle = angle - 1
                    kit.servo[my_gate.pin].angle = angle
                    if angle <= 70:
                        increase = True
                stdscr.addstr(cent_y, cent_x, str(angle))
                time.sleep(.02)
            if key == 'q':
                return True

            stdscr.refresh()
    
    def identify_gate(self, gate_key):
        '''takes gate_key and packages it in a wrapper to ship off to rattle_gate()'''
        my_gate = self.gates[gate_key]
        #print (f"Indentifying gate {my_gate.name} at {my_gate.location}")
        curses.wrapper(self.rattle_gate, gate_key)
        return True
    
    def set_location(self, gate_key):
        my_gate = self.gates[gate_key]
        print(f"Current location is {my_gate.location}")
        new_location = q.text("What is the location of this gate? 'q' to leave as is", style = style).ask()
        if new_location != 'q':
            self.gates[gate_key].location = new_location
            return True
        else:
            return False
    
    def set_all_gates(self):
        for g in self.gates:
            if not self.set_min(g):
                return False
            if not self.set_max(g):
                return False
        return True

    def set_gate(self, stdscr, gate_key, side):

        """ CURSES function so nees wrapping, create interface to adjust the gate"""

        my_gate = self.gates[gate_key]
        pin = my_gate.pin
        key = None
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

    def set_min(self, gate_key):
        gate_min = curses.wrapper(self.set_gate, gate_key, 'min')
        if gate_min != -1:
            self.gates[gate_key].min = gate_min
            return True
        else:
            print ("Changes abandoned")
            return False
    
    def set_max(self, gate_key):
        gate_max = curses.wrapper(self.set_gate, gate_key, 'max')
        if gate_max != -1:
            self.gates[gate_key].max = gate_max
            return True
        else:
            print ("Changes abandoned")
            return False

    def set_info(self, gate_key):
        my_gate = self.gates[gate_key]
        print(f"Current info is {my_gate.info}")
        new_info = q.text("Infomation about this gate? 'q' to leave as is", style = style).ask()
        self.gates[gate_key].info = new_info
        return True

    def remove_gate(self, gate_key):
        
        if self.delete_gate(gate_key):
            return True
        else:
            return False  

    def delete_gate(self, gate_key, confirm = True):
        my_gate= self.gates[gate_key]
        delete = False
        if confirm == True:
            delete = q.confirm(f"Are you sure you want to remove {my_gate.name} at location {my_gate.location}?", style = style).ask()
        if delete or not confirm:
            self.gates.pop(gate_key)
            return True
        else:
            print (f"Gate {my_gate.name} not removed.")
            return False

    def add_new_gate(self):
        number = len(self.gates)
        new_gate_object = Gate(
            'new',
            number,
            'unset',
            False,
            None,
            85,
            95,
            'New'
        )
        self.gates.update({'new': new_gate_object})
        self.modify_gate('new')
        
    def modify_gate(self, gate_key):
        if self.set_gate_pin(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_location(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_min(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_max(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_info(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_gate_name(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        return True

    def select_gate(self):
        gates_list = list ( self.gates.keys())
        gate_key = q.select("Which gate would you like to delete?",
                    choices = gates_list, 
                    default=None, 
                    qmark='?', 
                    pointer='»', 
                    style=style, 
                    use_shortcuts=False, 
                    use_arrow_keys=True, 
                    use_indicator=True, 
                    use_jk_keys=True, 
                    show_selected=True, 
                    instruction=None,).ask()
        return (gate_key)

def main_menu(gm):
    print("---------MAIN MENU----------")
    choices = ("view gates : compact",
                "view gates : extended", 
                "load gates", 
                "clear all gates", 
                "add gate", 
                "reorder gates", 
                "set all gates - min & max",
                "modify gate",
                "remove gate",
                "identify gate",
                "open all gates",
                "close all gates",
                "quit" )
    action = q.select("What do you want to do?",
                    choices = choices, 
                    default=None, 
                    qmark='?', 
                    pointer='»', 
                    style=style, 
                    use_shortcuts=True, 
                    use_arrow_keys=True, 
                    use_indicator=True, 
                    use_jk_keys=True, 
                    show_selected=True, 
                    instruction=None,).ask()
    if action == "view gates : compact":
        gm.view_gates_compact()
    
    elif action == "view gates : extended":
        gm.view_gates()
    
    elif action == "load gates":
        selected_file = gm.select_gates_file()
        gm.load_gates(selected_file)
        gm.write_gates('load_from_backup')
    
    elif action == "clear all gates":
        if gm.clear_gates():
            gm.write_gates('clear_all')
        else:
            print ("Gates not cleared")
    
    elif action == "add gate":
        if gm.add_new_gate():
            print (f"Gate added")
            gm.write_gates('gate_added')
        else:
            print ("Gate not added")
    
    elif action == "reorder gates":
        reodered_gates = reorder_dict.reorder(gm.gates)
        gm.gates = reodered_gates
        print("Gates reordered")
        gm.view_gates_compact()
        gm.write_gates(f"reordered")

    
    elif action == "set all gates - min & max":
        if gm.set_all_gates():
            print("All Gates Set")
        else:
            print("Only a few gates set")
        gm.write_gates('angles_set')
    
    elif action == 'modify gate':
        gate_key = gm.select_gate()
        if gm.modify_gate == True:
            print(f"Gate {gate_key} Modified")
            gm.write_gates(f"gate_{gate_key}_modified")



    elif action == "remove gate":
        gate_key = gm.select_gate()
        if gm.remove_gate(gate_key):
            print(f"Removed {gate_key} Gate")
            gm.write_gates(f"gate_{gate_key}_removed")
        else:
            print("Gate not removed")
    
    elif action == "identify gate":
        gate_key = gm.select_gate()
        gm.identify_gate(gate_key)
    elif action == "open all gates":
        pass
    elif action == "close all gates":
        pass
    elif action == "quit":
        sys.exit()

def main():
    gm = Gate_Manager(gates_file, backup_dir)
    print(f'LOADING GATES from {gm.gates_file} ')
    gm.view_gates_compact()
    while True:
        main_menu(gm)
        #gm.set_gate_name('T')





if __name__ == "__main__":
    main()