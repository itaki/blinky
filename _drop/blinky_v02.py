# keyboard version of blinky
import curses # for keyboard
import time
import blinky_bits
#from os.path import dirname, join



keyboard_present = True

def init():
    pass


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
            print('dusty is currently on')

        elif self.status == 'off':
            print('dusty was OFF and being turned on')
            self.status = 'on'
            # turn dustys relay pin on
            self.last_spin_up = time.time()

    def shutdown(self):
        if self.status != 'off':
            self.status = 'off'
            # turn off dusty relay pin
            print("============dusty in now turned off==================")

    def uptime(self):
        uptime = time.time() - self.last_spin_up
        return uptime
      


class Gate_manager:
    def __init__(self):
        pass

    def close_all_gates(self):
        for gate in gates:
            gates[gate].close()

    def open_all_gates(self):
        for gate in gates:
            gates[gate].open()

    def get_gate_settings(self):
        gate_settings = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        for tool in tools:
            if tools[tool].status != 'off':
                print(tools[tool].name, tools[tool].id_num, tools[tool].gate_prefs)
                i = 0
                for pref in tools[tool].gate_prefs:
                    #print(f'{pref} at index {i}')
                    if pref == 0:
                        gate_settings[i] = 0
                    i += 1
        print(f'New Gate Settings {gate_settings}')
        return gate_settings

    def set_gates(self, gate_settings):
        
        result = all(setting == 1 for setting in gate_settings)     #if all gates are closed emergency shutdown
        if (result):
            dusty.shutdown()
            print ('ALL GATES ARE CLOSED - GOING INTO EMERGENCY SHUT DOWN MODE')
        i=0
        for gate in gates:      
            #print(gate_settings[i])
            if gate_settings[i] == 0:
                gates[gate].open()
            else:
                gates[gate].close()
            #print(f'{gates[gate].name} set to {gates[gate].status}')
            i +=1


def key_getter(stdscr):
    """checking for keypress"""
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()


def tools_in_use():
    tools_on = []
    for tool in tools:
        if tools[tool].status != 'off':
            tools_on.append( tools[tool].name)
            print(f'{tools[tool].name} which is tool {tools[tool].id_num}' )
    return tools_on


def keyboard_manager(key):
    '''see which tool the keyboard has modified'''
    for tool in tools:
        # this only runs if it detects that the key pressed is a tool
        if key == tools[tool].keyboard_key:
            print(f'Tool {tools[tool].name} selected via Keyboard')
            if tools[tool].status == 'on':  # Tools is running so turn it off
                tools[tool].spindown()
                return
            else:
                tools[tool].turn_on()
                return


    else:
        print(f'key {key} not a tool')


def shop_manager():
    '''the shop manager takes the tools list and checks each one to seee what it needs to do'''
    for tool in tools:
        if tools[tool].flagged == True:             #if a tool has been flagged make sure to address it
        
            if tools[tool].status == 'on':
                if tools[tool].spin_down_time >= 0:
                    dusty.spinup()
                gate_settings = gatekeeper.get_gate_settings()
                gatekeeper.set_gates(gate_settings)
                tools[tool].flagged = False
                if tools[tool].spin_down_time < 0:
                    tools[tool].status = 'off'

        
            elif tools[tool].status == 'off':
                gate_settings = gatekeeper.get_gate_settings() 
                tools_on = tools_in_use()
                if tools_on: 
                    print(f'there are tools in use {tools_on}')
                    gatekeeper.set_gates(gate_settings)                  
                else:
                    print(f'there are NO tools in use ')        #check to see if any tools are on
                    dusty.shutdown()
                tools[tool].flagged = False
        
        if tools[tool].status == 'spindown':
            uptime = dusty.uptime()
            purge_time = time.time() - tools[tool].last_used
            if uptime < dusty.min_uptime:
                print (f'dustys min uptime is {dusty.min_uptime} but has only been on for {uptime}. WAITING...')
            elif purge_time > tools[tool].spin_down_time:
                tools[tool].turn_off()

################################################################################
# START APP HERE
################################################################################
tools = blinky_bits.get_tools('tools.json')
gates = blinky_bits.get_gates('gates.json')
dusty = Dust_collector('off', time.time(), 0, time.time(), min_uptime=2)  # create the dust collector
gatekeeper = Gate_manager()
tools['CloseAll'].status = "on"
tools['CloseAll'].flagged = True


while True:
    # check the keyboard for input
    if keyboard_present == True:  # O
        key = curses.wrapper(key_getter)
        if key != -1:  # if nothing selected
            # prints: 'key: 97' for 'a' pressed
            print(f'\r                           key: {key} pressed')
            # '-1' on no presses
            keyboard_manager(key)

    # run through all the tools to see if they are on
    shop_manager()

    time.sleep(.1)
