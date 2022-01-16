# keyboard version of blinky
import curses
import time
import json
from os.path import dirname, join

tools_list = []
tools = {}
gates_list = []  # list
gates = {}
keyboard_present = True


def get_file(filename):
    '''This gets a file associated in the working directory no matter where you run it.
        Useful for VSCode where the terminal doesn't always reside in the directory you are working out of.
        REQUIRES --- 
        from os.path import dirname, join

    '''
    current_dir = dirname(__file__)  # get current working directory
    file_path = join(current_dir, f"./{filename}")  # set file path
    return(file_path)


def init():

    # LOAD ALL THE TOOLS
    file_path = get_file('tools_list.json')  # set the file path
    with open(file_path, 'r') as f:  # read the tool list
        tools_list = json.load(f)  # load tool list into python

    for tool in tools_list:
        tools[tool['name']] = Tool(
            tool['id_num'],
            tool['name'],
            tool['status'],
            tool['gate_prefs'],
            tool['button_pin'],
            tool['voltage_pin'],
            tool['amp_trigger'],
            tool['keyboard_key'],
            tool['last_used'],
            tool['spin_down_time']
        )
        # 1print(tool)
    #print(f'These are your tools {tools}')

    # LOAD ALL THE GATES
    file_path = get_file('gates_list.json')  # set the file path
    with open(file_path, 'r') as f:  # read the gate list
        gates_list = json.load(f)  # load gate list into python

    for gate in gates_list:
        gates[gate['name']] = Gate(
            gate['name'],
            gate['location'],
            gate['min'],
            gate['max'],
        )
        # 1print(tool)
    #print(f'These are your tools {gates}')


class Tool:
    def __init__(self,
                 id_num,
                 name,
                 status=False,
                 gate_prefs=[False],
                 button_pin=0,
                 voltage_pin=12,
                 amp_trigger=10,
                 keyboard_key=0,
                 last_used=0,
                 spin_down_time=5):
        self.id_num = id_num
        self.name = name
        self.status = status
        self.gate_prefs = gate_prefs
        self.button_pin = button_pin
        self.voltage_pin = voltage_pin
        self.amp_trigger = amp_trigger
        self.keyboard_key = keyboard_key
        self.last_used = last_used
        self.spin_down_time = spin_down_time

    def turn_on(self):
        self.status = True
        print(f'{self.name} turned ON')
        gate_manager()
        dusty.spinup(self.spin_down_time)

    def turn_off(self):
        self.status = False
        print(f'{self.name} turned OFF')
        
        for tool in tools:
            if tools[tool].status == True:
                print(f'found a tool on = {tools[tool].name}')
                return

        print('No other tools on, sending spindown command')
        dusty.spindown()


class Dust_collector:
    def __init__(self, status, last_spin_up, spin_down_time, time_last_tool_went_off, min_uptime):
        self.status = 'off'
        self.last_spin_up = time.time()
        self.spin_down_time = 0
        self.time_last_tool_went_off = time.time()
        self.min_uptime = min_uptime

        # turn off dusty relay pin

    def spinup(self, spin_down_time=5):
        if self.status == 'on':  # dusty is currently on
            # check to see if the new spindown time is greater than the previous time
            if spin_down_time > self.spin_down_time:
                print(
                    f'replacing {self.spin_down_time} with new spin down time which is {spin_down_time}')
                # replace the spin_down_time with new spin_down_time
                self.spin_down_time = spin_down_time
        elif self.status == 'spindown':
            print('dusty was in spindown mode and now being reset to on')
            self.status = 'on'
            print(dusty.status, self.status)
            self.spin_down_time = spin_down_time
        elif self.status == 'off':
            print('dusty was OFF and being turned on')
            self.status = 'on'
            # turn dustys relay pin on
            self.last_spin_up = time.time()

            # check to see if the new spindown time is greater than the previous time
            if spin_down_time > self.spin_down_time:
                print(
                    f'replacing {self.spin_down_time} with new spin down time which is {spin_down_time}')
                # replace the spin_down_time with new spin_down_time
                self.spin_down_time = spin_down_time
            print(f'dusty was spun up at {self.last_spin_up}')

    def spindown(self):
        # this gets the time this function was called. Basically the time the tool went off.
        self.time_last_tool_went_off = time.time()
        self.status = 'spindown'
        print(
            f'-------------dusty is now in spindown mode---------------at  {self.time_last_tool_went_off}')

    def shutdown(self):
        if self.status != 'off':
            self.status = 'off'
            # turn off dusty relay pin
            print("============dusty in now turned off==================")
    
    def uptime(self):
        uptime = time.time() - self.last_spin_up
        return uptime


class Gate:
    def __init__(self, name, location, minimum, maximum):
        self.name = name
        self.location = location
        self.min = minimum
        self.max = maximum

    def open(self):
        print(f'opening {self.name}')
        # send maximum to gate

    def close(self):
        print(f'closing {self.name}')
        # send minimum to gate


class Gate_manager:
    def __init__(self):
        pass

    def close_all_gates():
        for gate in gates:
            gates[gate].close()

    def open_all_gates():
        for gate in gates:
            gates[gate].open()

    def set_gates():
        gate_settings = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        for tool in tools:
            if tools[tool].status == True:
                for i in tools[tool].gate_prefs:
                    if i == 0:
                        gate_settings[i] = 0;
        print ('New Gate Settings {gate_settings}')
        for i in gate_settings:
            gates[i].status = gate_settings[i].status
        for gate in gates:
            if gates[gate].status == 0:
                gates[gate].open()
            else:
                gates[gate].close()

def shop_manager():
    pass


def key_getter(stdscr):
    """checking for keypress"""
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()


def keyboard_manager(key):
    '''see which tool the keyboard has modified'''
    for tool in tools:
        # this only runs if it detects that the key pressed is a tool
        if key == tools[tool].keyboard_key:
            print(f'Tool {tools[tool].name} selected via Keyboard')
            if tools[tool].status == True:  # Tools is running so turn it off
                #print("running the turn off bit")
                tools[tool].turn_off()
            elif tools[tool].status == False:
                #print("running the turn on bit")
                tools[tool].turn_on()
            return(tool, tools[tool].status)
    else:
        print(f'key {key} not a tool')
        return('no_tool_selected', False)


################################################################################
# START APP HERE
################################################################################
init()
dusty = Dust_collector('off', time.time(), 0, time.time(),min_uptime=7)  # create the dust collector
gate_manager = Gate_manager()

while True:
    if keyboard_present == True:  # O
        key = curses.wrapper(key_getter)
        if key != -1:  # if nothing selected
            # prints: 'key: 97' for 'a' pressed
            print(f'\r                           key: {key} pressed')
            # '-1' on no presses
            change_state = keyboard_manager(key)
            print(change_state)

    if dusty.status == 'spindown':
        print(dusty.status)
        time_left = time.time() - dusty.time_last_tool_went_off
        if time_left > dusty.spin_down_time:
            dusty.shutdown()
        else:

            print(
                f'dusty in spindown mode and shuting down in {dusty.spin_down_time-time_left} seconds')

    time.sleep(1)
