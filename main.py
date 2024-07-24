import time 
import blinky_bits
import pygame
from pygame.locals import *
from gpiozero import LED, RGBLED, Button, DigitalOutputDevice
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from tool_manager import Tool_Manager
import voltage_sensor as vs
from gate_manager import Gate_Manager, get_full_path

# create some list of stuff I got
TOOLS_FILE = 'tools.json'
GATES_FILE = 'gates.json'
BACKUP_DIR = '_BU'

tm = Tool_Manager(TOOLS_FILE, BACKUP_DIR)
gm = Gate_Manager(GATES_FILE, BACKUP_DIR) # create the gate manager

num_of_buttons = len(tm.tools)
num_of_gates = len(gm.gates)

# set which interfaces to use

use_gui = True
use_buttons = False
use_voltage = True
use_collector = True


if use_gui: 
    '''intitalizes pygame canvas'''
    pygame.init()
    screen_width = 720
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('R.U.D.I the ShopBot')

    gates_width = 60
    terminal_height = 40
    num_of_tool_buttons_x = 3
    button_panel_width = screen_width-gates_width
    button_width = ((screen_width-gates_width)/num_of_tool_buttons_x)
    button_height = (screen_height-terminal_height) / (num_of_buttons/num_of_tool_buttons_x)
    gate_width = gate_height = (screen_height-terminal_height)/num_of_gates

    bg = '#16171d'
    clicked = False

if use_voltage:
    '''this activates the ADS1x15s and talks to the AC715s'''
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    start_address = 72  # ADS1115s start at 72 or 0x48
    max_volt_meters = 4  # there can only be a max of 4 ADS1115s
    cycles = 0  # sets the number of cycles to 0
    review_cycles = 6  # number of cycles the voltage has to drop below the trigger to confirm the tool is off

    tools_with_sensor = vs.get_tools_with_sensor(tm.tools)
    print(f"Tools with sensors: {tools_with_sensor}")

class Dust_collector:
    def __init__(self, pin, min_uptime):
        self.status = 'off'
        self.last_spin_up = time.time()
        self.min_uptime = min_uptime
        self.relay = DigitalOutputDevice(pin, active_high=True, initial_value=False)

    def spinup(self):
        if self.status == 'on':  # rosie is currently on
            pass
        elif self.status == 'off':
            self.status = 'on'
            self.relay.on()
            self.last_spin_up = time.time()

    def shutdown(self):
        if self.status != 'off':
            self.relay.off()
            self.status = 'off'

    def uptime(self):
        uptime = time.time() - self.last_spin_up
        return uptime


class Button_PG_gate():
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
        pygame.draw.rect(screen, self.on_col, self.button_rect,
                         border_radius=self.radius)

    def open_h(self):
        pygame.draw.rect(screen, self.on_col_h,
                         self.button_rect, border_radius=self.radius)

    def closed(self):
        pygame.draw.rect(screen, self.off_col, self.button_rect,
                         border_radius=self.radius)

    def closed_h(self):
        pygame.draw.rect(screen, self.off_col_h,
                         self.button_rect, border_radius=self.radius)

    def error(self):
        pygame.draw.rect(screen, self.error_col, self.button_rect,
                         border_radius=self.radius)

    def error_h(self):
        pygame.draw.rect(screen, self.error_col_h,
                         self.button_rect, border_radius=self.radius)

    def draw_button(self):
        global clicked
        action = False
        selected_gate = gm.gates[self.name] #select the gate associated with the button

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

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.button_rect = Rect(self.x+self.padding, self.y+self.padding,
                                self.width-(self.padding*2), self.height-(self.padding*2))

    def on(self):
        pygame.draw.rect(screen, self.on_col, self.button_rect,
                         border_radius=self.radius)

    def on_h(self):
        pygame.draw.rect(screen, self.on_col_h,
                         self.button_rect, border_radius=self.radius)

    def off(self):
        pygame.draw.rect(screen, self.off_col, self.button_rect,
                         border_radius=self.radius)

    def off_h(self):
        pygame.draw.rect(screen, self.off_col_h,
                         self.button_rect, border_radius=self.radius)

    def spindown(self):
        pygame.draw.rect(screen, self.spindown_col,
                         self.button_rect, border_radius=self.radius)

    def spindown_h(self):
        pygame.draw.rect(screen, self.spindown_col_h,
                         self.button_rect, border_radius=self.radius)

    def draw_button(self):
        global clicked
        action = False
        selected_tool = tm.tools[self.name] # select the tool associated with this button

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):  # mouse if over the button
            if pygame.mouse.get_pressed()[0] == 1:  # mouse is pressed but not released
                clicked = True
                if selected_tool.status == 'on':
                    self.spindown_h()
                elif selected_tool.status == 'off':
                    self.on_h()
                elif selected_tool.status == 'spindown':
                    self.on_h()
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:  # mouse was just released
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
            else:  # mouse is just over without click
                if selected_tool.status == 'on':
                    self.on_h()
                elif selected_tool.status == 'off':
                    self.off_h()
                elif selected_tool.status == 'spindown':
                    self.spindown_h()
        else:  # mouse is not over button
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


class Error(): # also know as Uniblab
    def __init__(self, name, time_stamp, error):
        self.object =  name
        self.time_stamp = time_stamp
        self.error = error


def create_tool_gui_buttons():
    x = 0
    y = 0
    gui_buttons = {}
    for tool in tm.tools:
        current_tool = tm.tools[tool]
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
    for gate in gm.gates:
        gate_buttons[gate] = Button_PG_gate(x,y,gate)
        x = x + gate_width
        if x >= button_panel_width:
            x = 0 + (screen_width - gates_width) + (gates_width/2)-(gate_width/2)
            y = y + gate_height

    return gate_buttons


def tools_in_use():
    tools_on = []
    for tool in tm.tools:
        current_tool = tm.tools[tool]
        if current_tool.status != 'off':
            tools_on.append(current_tool.name)
            print(f'{current_tool.name} which is tool {current_tool.id_num}' )
    return tools_on


def get_gate_settings(tools):
    open_gates = []
    for t in tools:
        current_tool = tools[t]
        if current_tool.status != 'off':
            for gate_pref in current_tool.gate_prefs:
                if gate_pref not in open_gates:
                    open_gates.append(gate_pref)
    return open_gates

    
def shop_manager():
    '''the shop manager takes the tools list and checks each one to see what it needs to do'''
    for tool in tm.tools:
        current_tool = tm.tools[tool]
        if current_tool.flagged == True:  # if a tool has been flagged make sure to address it
        
            if current_tool.status == 'on':
                if current_tool.spin_down_time >= 0:
                    rosie.spinup()
                gate_settings = get_gate_settings(tm.tools)  # this need to be a shop_manager method that talks to tools and then tells gm what to do
                gm.set_gates(gate_settings)
                current_tool.flagged = False
                if current_tool.spin_down_time < 0:  # use -1 to not turn tool on at all
                    current_tool.status = 'off'

            elif current_tool.status == 'off':
                opengates = get_gate_settings(tm.tools) 
                tools_on = tools_in_use()
                if tools_on: 
                    print(f'There are tools in use {tools_on}')
                    gm.set_gates(opengates)                  
                else:
                    print(f'There are NO tools in use ')  # check to see if any tools are on
                    rosie.shutdown()
                current_tool.flagged = False
        
        if current_tool.status == 'spindown':
            uptime = rosie.uptime()
            purge_time = time.time() - current_tool.last_used
            if uptime < rosie.min_uptime:
                pass            
            elif purge_time > current_tool.spin_down_time:
                current_tool.turn_off()

################################################################################
# START APP HERE
################################################################################
min_uptime = 10  # smallest amount of time the dust collector can be on for
used_pins = tm.get_used_pins()
collector_pin = 25
if collector_pin in used_pins:
    tool_using_pin = tm.whats_on_pin(collector_pin)
    print(f"The assigned collector pin {collector_pin} is being used by {tool_using_pin} ")
    print(f"The used pins are {used_pins}")
    exit()
rosie = Dust_collector(collector_pin, min_uptime)  # create the dust collector

if use_gui:
    gui_buttons = create_tool_gui_buttons()
    gate_buttons = create_gate_gui_buttons()

run = True

if __name__ == '__main__':
    while run:
        if use_gui:
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
                    pass
                    #keyboard_manager(event.key)
                elif event.type == pygame.QUIT:
                    run = False        
            pygame.display.update()

        if use_voltage:
            for tool in tools_with_sensor:
                selected_tool = tm.tools[tool]
                if selected_tool.override == False:
                    am_i_on = selected_tool.voltage_sensor.am_i_on()
                    if am_i_on and selected_tool.status != 'on':
                        selected_tool.turn_on()
                    elif not am_i_on and selected_tool.status == 'on':
                        selected_tool.spindown()

        # run through all the tools to see if they are on
        shop_manager()
    
    pygame.quit()
