import time 
import blinky_bits
import pygame
from pygame.locals import *
from gpiozero import LED, RGBLED, Button
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# from os.path import dirname, join

# create some list of shit I got
tools_file = 'tools.json'
gates_file = 'gates.json'
#tools_file = 'tools_large_number.json'
#gates_file = 'gates_large_number.json'
tools = blinky_bits.get_tools(tools_file)
gates = blinky_bits.get_gates(gates_file)
num_of_buttons = len(tools)
num_of_gates = len(gates)

# set which interfaces to use

use_gui = True
use_buttons = False
use_voltage = False

if use_gui: 
    '''intitalizes pygame canvas'''
    pygame.init()

    screen_width = 400
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('BLINKY')

    gates_width = 60
    terminal_height = 40
    num_of_tool_buttons_x = 3
    button_panel_width = screen_width-gates_width
    button_width = ((screen_width-gates_width)/num_of_tool_buttons_x)
    button_height = (screen_height-terminal_height) / \
                     (num_of_buttons/num_of_tool_buttons_x)
    gate_width = gate_height = (screen_height-terminal_height)/num_of_gates

    bg = '#16171d'
    # red = '#19d1e5'
    # black = (0, 0, 0)
    # white = (255, 255, 255)
    clicked = False

if use_voltage:
    '''this activates the ADS1115 and talks to the AC715'''
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)

    cycles = 0 # sets the number of cycles to 0
    review_cycles = 6 # number of cycles the voltage has to drop below the trigger to confirm the tool is off



def init():
    pass


class Dust_collector:
    def __init__(self, status, last_spin_up, min_uptime):
        self.status = 'off'
        self.last_spin_up = time.time()
        self.min_uptime = min_uptime

        # turn off dusty relay pin

    def spinup(self):
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
        gate_settings = []
        for i in range(num_of_gates):
            gate_settings.append(1)
        for tool in tools:
            current_tool = tools[tool]
            if current_tool.status != 'off':
                print(current_tool.name, current_tool.id_num,
                      current_tool.gate_prefs)
                i = 0
                for pref in current_tool.gate_prefs:
                    # print(f'{pref} at index {i}')
                    if pref == 0:
                        gate_settings[i] = 0
                    i += 1
        print(f'New Gate Settings {gate_settings}')
        return gate_settings

    def set_gates(self, gate_settings):

        # if all gates are closed emergency shutdown
        result = all(setting == 1 for setting in gate_settings)
        if (result):
            dusty.shutdown()
            print('ALL GATES ARE CLOSED - MAKING SURE DUSTY IS SHUT DOWN')
        i = 0
        for gate in gates:
            current_gate = gates[gate]
            # print(gate_settings[i])
            if gate_settings[i] != 1:
                current_gate.open()
            else:
                current_gate.close()
            # print(f'{gates[gate].name} set to {gates[gate].status}')
            i += 1


class Button_PG_gate():
    padding = 4
    radius = 7
    padding = 4
    radius = 7
    off_col = '#19d1e5'
    off_col_h = '#29e1e6'
    on_col = '#81f900'
    on_col_h = '#82f102'
    error_col = '#ff3f4f'
    error_col_h = '#ff4050'
    text_col = '#16171d'
    width = gate_width
    height = gate_height
    font_size = 16
    font = pygame.font.SysFont('meslolgsnf', font_size, bold=True)

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.button_rect = Rect(self.x+self.padding, self.y+self.padding,
                                self.width-(self.padding*2), self.height-(self.padding*2))

    def open(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col, self.button_rect,
                         border_radius=self.radius)

    def open_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col_h,
                         self.button_rect, border_radius=self.radius)

    def closed(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col, self.button_rect,
                         border_radius=self.radius)

    def closed_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col_h,
                         self.button_rect, border_radius=self.radius)

    def error(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col, self.button_rect,
                         border_radius=self.radius)

    def error_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col_h,
                         self.button_rect, border_radius=self.radius)

    def draw_button(self):
        global clicked
        action = False
        selected_gate = gates[self.name] #select the gate associated with the button

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):  # mouse if over the button
            # mouse is pressed but not released
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                if selected_gate.status == 1:
                    self.closed_h()
                elif selected_gate.status == 0:
                    self.open_h()
                elif selected_gate.status == -1:
                    self.error_h()
            # mouse was just released
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                if selected_gate.status == 1:
                    # open the info window HERE
                    info_window.status = True 
                    info_window.gate = self
                    pass

                clicked = False
                action = True
            else:  # mouse is just over without click
                if selected_gate.status == 1:
                    self.open_h()
                elif selected_gate.status == 0:
                    self.closed_h()
                elif selected_gate.status == -1:
                    self.error_h()

        else:  # mouse is not over button
            if selected_gate.status == 1:
                self.closed()
            elif selected_gate.status == 0:
                self.open()
            elif selected_gate.status == -1:
                self.error()

        # add text to button
        text_img = self.font.render(self.name, True, self.text_col)
        text_len = text_img.get_width()

        screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), self.y + ((self.font_size/2) + 2)))


        return action


class Button_PG_tool():


    # colours for button and text
    padding = 4
    radius = 7
    off_col = '#19d1e5'
    off_col_h = '#29e1e6'
    on_col = '#81f900'
    on_col_h = '#82f102'
    spindown_col = '#ff9700'
    spindown_col_h = '#ff9801'
    text_col = '#16171d'
    width = button_width
    height = button_height
    status = False
    font_size = 14
    font = pygame.font.SysFont('meslolgsnf', font_size, bold=True)
    #font = pygame.font.SysFont('Menlo', 20, bold=True)

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.button_rect = Rect(self.x+self.padding, self.y+self.padding,
                                self.width-(self.padding*2), self.height-(self.padding*2))

    def on(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col, self.button_rect,
                         border_radius=self.radius)

    def on_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col_h,
                         self.button_rect, border_radius=self.radius)

    def off(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col, self.button_rect,
                         border_radius=self.radius)

    def off_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col_h,
                         self.button_rect, border_radius=self.radius)

    def spindown(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.spindown_col,
                         self.button_rect, border_radius=self.radius)

    def spindown_h(self):
        # button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.spindown_col_h,
                         self.button_rect, border_radius=self.radius)

    def draw_button(self):
        global clicked
        action = False
        selected_tool = tools[self.name] # select the tool associated with this button

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):                             #mouse if over the button

            if pygame.mouse.get_pressed()[0] == 1:                       #mouse is pressed but not released
                clicked = True
                if selected_tool.status == 'on':
                    self.spindown_h()
                elif selected_tool.status == 'off':
                    self.on_h()
                elif selected_tool.status == 'spindown':
                    self.on_h()
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True: #mouse was just released
                if selected_tool.status == 'on':
                    selected_tool.override = False
                    selected_tool.spindown()
                    self.spindown_h()
                elif selected_tool.status != 'on':
                    selected_tool.turn_on()
                    selected_tool.override = True
                    self.on_h()

                clicked = False
                action = True
            else:                                                       #mouse is just over without click
                if selected_tool.status == 'on':
                    self.on_h()
                elif selected_tool.status == 'off':
                    self.off_h()
                elif selected_tool.status == 'spindown':
                    self.spindown_h()
        else:                                                           #mouse is not over button
            if selected_tool.status == 'on':
                self.on()
            elif selected_tool.status == 'off':
                self.off()
            elif selected_tool.status == 'spindown':
                self.spindown()

        # add text to button
        text_img = self.font.render(self.name, True, self.text_col)
        text_len = text_img.get_width()

        if selected_tool.status == 'spindown':
            info = str(round(selected_tool.spin_down_time - 
                                    (time.time() - selected_tool.last_used), 1))
        elif selected_tool.status == 'on':
            info = 'on'
        else:
            info = 'off'
        
        status_line = self.font.render(info, True, self.text_col)
        status_len = status_line.get_width()
        center_y = self.y + (self.height / 2)
        screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), center_y - (self.font_size + 2)))
        screen.blit(status_line, (self.x + int(self.width / 2) -
                    int(status_len / 2), center_y + 1))
        return action


class Error():
    def __init__(self, name, time_stanp, error):
        self.object =  name
        self.time_stanp = time_stanp
        self.error = error



def create_tool_gui_buttons():
    x = 0
    y = 0
    gui_buttons = {}
    for tool in tools:
        current_tool = tools[tool]
        gui_buttons[current_tool.name] = Button_PG_tool(x,y,current_tool.name)
        x = x + button_width
        if x >= button_panel_width:
            x = 0
            y = y + button_height

    return gui_buttons


def create_gate_gui_buttons():
    x = 0 + (screen_width - gates_width) + (gates_width/2)-(gate_width/2)
    y = 0
    gate_buttons = {}
    for gate in gates:
        current_gate = gates[gate]
        gate_buttons[gates[gate].name] = Button_PG_gate(x,y,gates[gate].name)
        x = x + button_width
        if x >= button_panel_width:
            x = 0 + (screen_width - gates_width) + (gates_width/2)-(gate_width/2)
            y = y + gate_height

    return gate_buttons

def create_real_buttons():
    for tool in tools:
        # select the tool I'm currently working with
        current_tool = tools[tool]
        if current_tool.button_pin != 0:
            print(f"Creating {current_tool.name} on {current_tool.button_pin}")
            #create a button object and put it in the dictionary
            current_tool.btn = Button(current_tool.button_pin)
            current_tool.btn.when_pressed = current_tool.button_cycle
            if current_tool.led_type == "RGB":
                current_tool.led = RGBLED(current_tool.r_pin, current_tool.g_pin, current_tool.b_pin)
                print(f"created RGBLED on {current_tool.r_pin, current_tool.g_pin, current_tool.b_pin}")
                #current_tool.led.color = (.1,.82,.90)
            elif current_tool.led_type == "LED":
                current_tool.led = LED(current_tool.r_pin)
                print(f"created LED on {current_tool.r_pin}")
            else:
                print(f"no button created for {current_tool.name}")
            

def create_voltage_switchs():
    for tool in tools:
        current_tool = tools[tool]
        if current_tool.voltage_pin != 0:
            pin = current_tool.voltage_pin
            current_tool.chan = AnalogIn(ads, ADS.P0)


def tools_in_use():
    tools_on = []
    for tool in tools:
        current_tool = tools[tool]
        if current_tool.status != 'off':
            tools_on.append( current_tool.name)
            print(f'{current_tool.name} which is tool {current_tool.id_num}' )
    return tools_on


def keyboard_manager(key):
    '''see which tool the keyboard has modified'''
    for tool in tools:
        # this only runs if it detects that the key pressed is a tool
        current_tool = tools[tool]
        if key == current_tool.keyboard_key:
            print(f'Tool {current_tool.name} selected via Keyboard')
            if current_tool.status == 'on':  # Tools is running so turn it off
                current_tool.spindown()
                return
            else:
                current_tool.turn_on()
                return


    else:
        print(f'key {key} not a tool')

def info_window():
    pass
    
def shop_manager():
    '''the shop manager takes the tools list and checks each one to see what it needs to do'''
    for tool in tools:
        current_tool = tools[tool]
        if current_tool.flagged == True:             #if a tool has been flagged make sure to address it
        
            if current_tool.status == 'on':
                if current_tool.spin_down_time >= 0:
                    dusty.spinup()
                gate_settings = gatekeeper.get_gate_settings()
                gatekeeper.set_gates(gate_settings)
                current_tool.flagged = False
                if current_tool.spin_down_time < 0: #use -1 to not turn tool on at all
                    current_tool.status = 'off'

        
            elif current_tool.status == 'off':
                gate_settings = gatekeeper.get_gate_settings() 
                tools_on = tools_in_use()
                if tools_on: 
                    print(f'there are tools in use {tools_on}')
                    gatekeeper.set_gates(gate_settings)                  
                else:
                    print(f'there are NO tools in use ')        #check to see if any tools are on
                    dusty.shutdown()
                current_tool.flagged = False
        
        if current_tool.status == 'spindown':
            uptime = dusty.uptime()
            purge_time = time.time() - current_tool.last_used
            if uptime < dusty.min_uptime:
                # print (f'dustys min uptime is {dusty.min_uptime} but has only been on for {uptime}. WAITING...')
                pass            
            elif purge_time > current_tool.spin_down_time:
                current_tool.turn_off()

################################################################################
# START APP HERE
################################################################################
min_uptime = 5 #smallest amount of time the dust collector can be on for
dusty = Dust_collector('off', time.time(), min_uptime)  # create the dust collector
gatekeeper = Gate_manager() # create the gate manager
#tools['CloseAll'].status = "on"
#tools['CloseAll'].flagged = True

if use_gui:
    gui_buttons = create_tool_gui_buttons()
    gate_buttons = create_gate_gui_buttons()

if use_buttons:
    create_real_buttons()

if use_voltage:
    create_voltage_switchs()


run = True


while run:
    
    if use_gui: #
        '''this runs pygame and draws all the buttons on every cycle'''
        screen.fill(bg)
        for button in gui_buttons:
            if gui_buttons[button].draw_button():
                pass
        for gate in gate_buttons: 
            if gate_buttons[gate].draw_button():
                pass
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keyboard_manager(event.key)
            elif event.type == pygame.QUIT:
                run = False        
        pygame.display.update()

    if use_voltage:
        for tool in tools:
            current_tool = tools[tool]
            if current_tool.override == False:
                if current_tool.voltage_pin != 0: # only check for tools that are on the amp trigger
                    
                    if current_tool.chan.voltage >= current_tool.amp_trigger:
                        cycles = 0
                        if current_tool.status != "on":
                            print(current_tool.chan.voltage)
                            current_tool.turn_on()
                    elif current_tool.chan.voltage < current_tool.amp_trigger and current_tool.status == "on":
                        if cycles >= review_cycles:
                            print(current_tool.chan.voltage)
                            current_tool.spindown()
                            cycles = 0
                        else:
                            cycles = cycles + 1
    # run through all the tools to see if they are on
    shop_manager()
    

pygame.quit()
