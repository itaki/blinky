import time
import blinky_bits
import pygame
from pygame.locals import *

# from os.path import dirname, join

# create some list of shit I got
tools_file = 'tools.json'
gates_file = 'gates.json'
tools = blinky_bits.get_tools(tools_file)
gates = blinky_bits.get_gates(gates_file)
num_of_buttons = len(tools)
num_of_gates = len(gates)

# set which interfaces to use

use_gui = True

if use_gui:
    pygame.init()

    screen_width = 240
    screen_height = 320
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('BLINKY')

    gates_width = 60
    terminal_height = 40
    num_of_tool_buttons_x = 2
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
        gate_settings = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        for tool in tools:
            if tools[tool].status != 'off':
                print(tools[tool].name, tools[tool].id_num,
                      tools[tool].gate_prefs)
                i = 0
                for pref in tools[tool].gate_prefs:
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
            # print(gate_settings[i])
            if gate_settings[i] == 0:
                gates[gate].open()
            else:
                gates[gate].close()
            # print(f'{gates[gate].name} set to {gates[gate].status}')
            i += 1


class Gate_button():
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
    font = pygame.font.SysFont('Menlo', 6, bold=False)

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

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):  # mouse if over the button
            # mouse is pressed but not released
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                if gates[self.name].status == 1:
                    self.closed_h()
                elif gates[self.name].status == 0:
                    self.open_h()
                elif gates[self.name].status == -1:
                    self.error_h()
            # mouse was just released
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                if gates[self.name].status == 1:
                    # open the info window HERE
                    info_window.status = True 
                    info_window.gate = self
                    pass

                clicked = False
                action = True
            else:  # mouse is just over without click
                if gates[self.name].status == 1:
                    self.open_h()
                elif gates[self.name].status == 0:
                    self.closed_h()
                elif gates[self.name].status == -1:
                    self.error_h()

        else:  # mouse is not over button
            if gates[self.name].status == 1:
                self.closed()
            elif gates[self.name].status == 0:
                self.open()
            elif gates[self.name].status == -1:
                self.error()

        # add text to button
        text_img = self.font.render(self.name, True, self.text_col)
        text_len = text_img.get_width()

        # if gates[self.name].status == 'spindown':
        #     info = str(round(tools[self.name].spin_down_time -
        #                             (time.time() - tools[self.name].last_used), 1))
        # elif tools[self.name].status == 'on':
        #     info = 'on'
        # else:
        #     info = 'off'

        # status_line = self.font.render(info, True, self.text_col)
        # status_len = status_line.get_width()

        # screen.blit(text_img, (self.x + int(self.width / 2) -
        #             int(text_len / 2), self.y +5))
        # screen.blit(status_line, (self.x + int(self.width / 2) -
        #             int(status_len / 2), self.y +25))
        return action


class Tool_button():


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
    font = pygame.font.SysFont('meslolgsnf', 10, bold=True)
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

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):                             #mouse if over the button
            if pygame.mouse.get_pressed()[0] == 1:                       #mouse is pressed but not released
                clicked = True
                if tools[self.name].status == 'on':
                    self.spindown_h()
                elif tools[self.name].status == 'off':
                    self.on_h()
                elif tools[self.name].status == 'spindown':
                    self.on_h()
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True: #mouse was just released
                if tools[self.name].status == 'on':
                    tools[self.name].spindown()
                    self.spindown_h()
                elif tools[self.name].status == 'off':
                    tools[self.name].turn_on()
                    self.on_h()
                elif tools[self.name].status == 'spindown':
                    tools[self.name].turn_on()
                    self.on_h()
                clicked = False
                action = True
            else:                                                       #mouse is just over without click
                if tools[self.name].status == 'on':
                    self.on_h()
                elif tools[self.name].status == 'off':
                    self.off_h()
                elif tools[self.name].status == 'spindown':
                    self.spindown_h()
        else:                                                           #mouse is not over button
            if tools[self.name].status == 'on':
                self.on()
            elif tools[self.name].status == 'off':
                self.off()
            elif tools[self.name].status == 'spindown':
                self.spindown()

        # add text to button
        text_img = self.font.render(self.name, True, self.text_col)
        text_len = text_img.get_width()

        if tools[self.name].status == 'spindown':
            info = str(round(tools[self.name].spin_down_time - 
                                    (time.time() - tools[self.name].last_used), 1))
        elif tools[self.name].status == 'on':
            info = 'on'
        else:
            info = 'off'
        
        status_line = self.font.render(info, True, self.text_col)
        status_len = status_line.get_width()
        
        screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), self.y +12))
        screen.blit(status_line, (self.x + int(self.width / 2) -
                    int(status_len / 2), self.y +25))
        return action


class Error():
    def __init__(self, name, time_stanp, error):
        self.object =  name
        self.time_stanp = time_stanp
        self.error = error



def create_tool_buttons():
    x = 0
    y = 0
    gui_buttons = {}
    for tool in tools:
        gui_buttons[tools[tool].name] = Tool_button(x,y,tools[tool].name)
        x = x + button_width
        if x >= button_panel_width:
            x = 0
            y = y + button_height

    return gui_buttons


def create_gate_buttons():
    x = 0 + (screen_width - gates_width) + (gates_width/2)-(gate_width/2)
    y = 0
    gate_buttons = {}
    for gate in gates:
        gate_buttons[gates[gate].name] = Gate_button(x,y,gates[gate].name)
        x = x + button_width
        if x >= button_panel_width:
            x = 0 + (screen_width - gates_width) + (gates_width/2)-(gate_width/2)
            y = y + gate_height

    return gate_buttons


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

def info_window():
    pass
    
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
                if tools[tool].spin_down_time < 0: #use -1 to not turn tool on at all
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
                # print (f'dustys min uptime is {dusty.min_uptime} but has only been on for {uptime}. WAITING...')
                pass            
            elif purge_time > tools[tool].spin_down_time:
                tools[tool].turn_off()

################################################################################
# START APP HERE
################################################################################
min_uptime = 5 #smallest amount of time the dust collector can be on for
dusty = Dust_collector('off', time.time(), min_uptime)  # create the dust collector
gatekeeper = Gate_manager() # create the gate manager
tools['CloseAll'].status = "on"
tools['CloseAll'].flagged = True

if use_gui:
    gui_buttons = create_tool_buttons()
    gate_buttons = create_gate_buttons()



run = True


while run:
    
    if use_gui: #
        screen.fill(bg)
        for button in gui_buttons:
            if gui_buttons[button].draw_button():
                pass
        for gate in gate_buttons: 
            if gate_buttons[gate].draw_button():
                pass

        # counter_img = button_font.render(str(counter), True, red)
        # screen.blit(counter_img, (200, 250))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keyboard_manager(event.key)
            elif event.type == pygame.QUIT:
                run = False
        
        shop_manager()
        
        pygame.display.update()


    # run through all the tools to see if they are on
    # shop_manager()

    

pygame.quit()
