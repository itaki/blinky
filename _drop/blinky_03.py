#keyboard version of blinky
import curses
import time
import json
from os.path import dirname, join

tools_list = []
tools = {}
gates_list = [] # list
gates = {}
keyboard_present = True

def get_file(filename):
    '''This gets a file associated in the working directory no matter where you run it.
        Useful for VSCode where the terminal doesn't always reside in the directory you are working out of.
        REQUIRES --- 
        from os.path import dirname, join
        
    '''
    current_dir = dirname(__file__)                         #get current working directory
    file_path = join(current_dir, f"./{filename}")          #set file path
    return(file_path)

def init(): #
    
    ######## LOAD ALL THE TOOLS
    file_path = get_file('tools_list.json')                 #set the file path
    with open(file_path, 'r') as f:                         #read the tool list
        tools_list = json.load(f)                           #load tool list into python
    
    for tool in tools_list: #
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
        #1print(tool)
    print(f'These are your tools {tools}')

    ######## LOAD ALL THE GATES
    file_path = get_file('gates_list.json')                 #set the file path
    with open(file_path, 'r') as f:                         #read the gate list
        gates_list = json.load(f)                           #load gate list into python
    
    for gate in gates_list: #
        gates[gate['name']] = Gate( 
            gate['name'],
            gate['location'], 
            gate['min'], 
            gate['max'], 
            ) 
        #1print(tool)
    print(f'These are your tools {gates}')
    

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
                spin_down_time=5 ):
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
    
    def turn_on():
        dusty = on

class Dust_collector:
    def __init__(self,status,last_spin_up,spin_down_time,time_last_tool_went_off):
        self.status = 'off'
        self.last_spin_up = time.time()
        self.spin_down_time = 0
        self.time_last_tool_went_off = time.time()


         #turn off dusty relay pin
    
    def spinup(self,spin_down_time=5):
        if self.status == 'on':   #dusty is currently on
            if spin_down_time > self.spin_down_time:  #check to see if the new spindown time is greater than the previous time
                print(f'replacing {self.spin_down_time} with new spin down time which is {spin_down_time}')
                self.spin_down_time = spin_down_time        #replace the spin_down_time with new spin_down_time      
        elif self.status == 'spindown':
            print('dusty was in spindown mode and now being reset to on')
            self.staus = 'on'
            self.last_spin_up = time.time()
            self.spin_down_time = spin_down_time
        elif self.status == 'off':
            print('dusty was OFF and being turned on')
            self.staus = 'on'
            ######turn dustys relay pin on
            self.last_spin_up = time.time()

            if spin_down_time > self.spin_down_time:  #check to see if the new spindown time is greater than the previous time
                print(f'replacing {self.spin_down_time} with new spin down time which is {spin_down_time}')
                self.spin_down_time = spin_down_time        #replace the spin_down_time with new spin_down_time  
            print (f'dusty was spun up at {self.last_spin_up}')

    
    def spindown(self):
        self.time_last_tool_went_off = time.time()          #this gets the time this function was called. Basically the time the tool went off.
        self.status = 'spindown'
        print(f'-------------dusty is now in spindown mode---------------at  {self.time_last_tool_went_off}')
    
    def shutdown(self):
        if self.status != 'off':
            self.status = 'off'
            #turn off dusty relay pin
            print("============dusty in now turned off==================")

class Gate:
        def __init__(self, name,location,minimum,maximum):
            self.name = name
            self.location = location
            self.min = minimum #
            self.max = maximum
        def open(self): #
            print(f'opening {self.name}')
            #send maximum to gate
        def close(self): #
            print(f'closing {self.name}')
            #send minimum to gate


def shop_manager(): #
    pass

def key_getter(stdscr):
    """checking for keypress"""
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()

def keyboard_action(key): #
    '''see which tool the keyboard has modified'''
    for tool in tools: #
        if key == tools[tool].keyboard_key:         #this only runs if it detects that the key pressed is a tool
            print (f'Tool {tools[tool].name} selected')
            if tools[tool].status == True:          #Tools is running so turn it off
                print (f'{tool} turned OFF')
                tools[tool].status = False          #Set the tools status to off
                dusty.spindown()                    #tell dusty to spindown
    
            elif tools[tool].status == False: 
                print (f'{tool} turned ON')
                tools[tool].status = True
                dusty.spinup(tools[tool].spin_down_time)
            return(tool, tools[tool].status)
    else:
        print (f'key {key} not a tool') 
        return('no_tool_selected', False)


init()
dusty = Dust_collector('off',time.time(),0,time.time())                                #create the dust collector

while True:
    if keyboard_present == True:                       #O
        key = curses.wrapper(key_getter)
        if key != -1:                                           #if nothing selected
            print(f'\r                           key: {key} pressed' ) # prints: 'key: 97' for 'a' pressed
                                            # '-1' on no presses
            change_state = keyboard_action(key)
            print(change_state)
            
    if dusty.status == 'spindown':
        print(f'dusty last went offf {dusty.time_last_tool_went_off}')
        time_left = time.time() - dusty.time_last_tool_went_off
        print(f'time since last tool went off {time_left}')
        print(dusty.spin_down_time)
        if time_left > dusty.spin_down_time:
            dusty.shutdown()
        else:
        
            print(f'dusty in spindown mode and shuting down in {dusty.spin_down_time-time_left} seconds')

            
    
    # for tool in tools:
    #     if tools[tool].status == True:
    #         dusty.spinup(tools[tool].spin_down_time) #
    #     statuss = [];
    #     statuss.append(tools[tool].status)

    #     if True not in statuss:
    #         dusty.shutdown()


        

        
                     #


    time.sleep(1)
