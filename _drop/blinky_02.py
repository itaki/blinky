#keyboard version of blinky
import curses
import time
import json
from os.path import dirname, join

tool_ids = []
tool_names = []

def init(): #
    current_dir = dirname(__file__)                         #get current working directory
    file_path = join(current_dir, "./tools_list.json")      #set the file path
    with open(file_path, 'r') as tools_list:                #read the tool list
        tools = json.load(tools_list)                       #load tool list into python
    
    #dump = json.dumps(tools, indent=4)
    #print(dump)

    #try building each tool
    for tool in tools:
        tool_ids.append(tool['keyboard_key'])               # build a list of keyboard keys
        tool_names.append(tool['name'])                     # build a list of tools by name
        tool['name'] = Tool(tool['id_num'],tool['name'])
        print (tool['name'].name)
        print (tool['name'].gate_prefs)
        print (tool['name'].spin_down_time)


class Tool:
    def __init__(self, id_num, name, status=False, gate_prefs=[False], sensor_type='keyboard', sensor_pin=12, amp_trigger=10, last_used=0, spin_down_time=5 ):
        self.id_num = id_num
        self.name = name
        self.status = status
        self.gate_prefs = gate_prefs
        self.sensor_type = sensor_type
        self.sensor_pin = sensor_pin
        self.amp_trigger = amp_trigger
        self.last_used = last_used
        self.spin_down_time = spin_down_time
    def am_i_on(self):
        if (self.sensor_type == 'button'):
            if (self.button_pressed == True):
                if (self.status == 'on'):
                    status = 'spindown'
                    last_used = time.getTime()
                else:
                    status ='on'
        elif (self.sensor_type == 'voltage'):
            amps = self.voltage_sensor.get_amps(self.pin_number)
            if (amps < self.amp_trigger):
                if (self.status == 'on'):
                    status = 'spindown'
                    last_used = time.getTime()
            elif (amps > self.amp_trigger):
                self.status 



def key_getter(stdscr):
    """checking for keypress"""
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()


init()

while True:
    key = curses.wrapper(key_getter)
    if key != -1: #
        print(f'key: {key}' ) # prints: 'key: 97' for 'a' pressed
                                        # '-1' on no presses
        if key in tool_ids: #
            for tool in tools: #
                if key == tool['keyboard_key']:
                    if tool['status'] == True: #
                        tools['status'] == False
                    else: #
                        tool['status'] == True
        else:
            print (f'key {key} not a tool')

    time.sleep(.1)
