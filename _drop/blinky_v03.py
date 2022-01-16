import curses # for keyboard
import time
import blinky_bits
import pygame
from pygame.locals import *
#from os.path import dirname, join

# create some list of shit I got
tools_file = 'tools.json'
gates_file = 'gates.json'
tools = blinky_bits.get_tools(tools_file)
gates = blinky_bits.get_gates(gates_file)
num_of_buttons = len(tools)


#set which interfaces to use
use_keyboard = False
use_gui = True

if use_gui:
    pygame.init()
    font = pygame.font.SysFont('Menlo', 6, bold=False)
    button_font = pygame.font.SysFont('Menlo', 10, bold=True)
    screen_width = 240
    screen_height = 320
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('BLINKY')


    gates_width = 60
    terminal_height = 40
    num_of_tool_buttons_x = 2
    button_panel_width = screen_width-gates_width
    button_width = ((screen_width-gates_width)/num_of_tool_buttons_x)
    button_height = (screen_height-terminal_height)/(num_of_buttons/num_of_tool_buttons_x)


    bg = '#16171d'
    #red = '#19d1e5'
    #black = (0, 0, 0)
    #white = (255, 255, 255)
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
            print ('ALL GATES ARE CLOSED - MAKING SURE DUSTY IS SHUT DOWN')
        i=0
        for gate in gates:      
            #print(gate_settings[i])
            if gate_settings[i] == 0:
                gates[gate].open()
            else:
                gates[gate].close()
            #print(f'{gates[gate].name} set to {gates[gate].status}')
            i +=1


class Gui_button():

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
    
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
    
    def on(self):
        #button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col, self.button_rect, border_radius=self.radius)

    def hover_on(self):
        #button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.on_col_h, self.button_rect, border_radius=self.radius)

    def off(self):
        #button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col, self.button_rect, border_radius=self.radius)
    
    def hover_off(self):
        #button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.off_col_h, self.button_rect, border_radius=self.radius)
    
    def spindown(self):
        #button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.spindown_col, self.button_rect, border_radius=self.radius)
    
    def spindown_hover(self):
        #button_rect = Rect(self.x+self.padding, self.y+self.padding, self.width-(self.padding*2), self.height-(self.padding*2))
        pygame.draw.rect(screen, self.spinddown_col_h, self.button_rect, border_radius=self.radius)

    def draw_button(self):
        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button

        # check mouseover and clicked conditions
        if self.button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                if tools[self.name].status == 'on':
                    self.hover_spindown()
                elif tools[self.name].status == 'off': 
                    self.hover_on()
                elif tools[self.name].status == 'spindown':
                    self.hover_on()
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                if self.status == False:
                    #turn on the tool
                    self.on()
                    self.status = True
                else: #turn off
                    #turn off the tool
                    self.off()
                    self.status = False
                clicked = False
                action = True
            else:
                if self.status == True:
                    self.hover_on()
                else: 
                    self.hover_off()
        else:
            if tools[self.name].status == False:
                self.off()
            else: # status
                self.on()
        # add shading to button
        # pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        # pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        # pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        # pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = button_font.render(self.name, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), self.y + 25))
        return action

def get_gui_buttons():
    x = 0
    y = 0
    gui_buttons = {}
    for tool in tools:
        gui_buttons[tools[tool].name] = Gui_button(x,y,tools[tool].name)
        x = x + button_width
        if x >= button_panel_width:
            x = 0
            y = y + button_height

    return gui_buttons

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
                if tools[tool].spin_down_time < 0: #use -1 in the json file to have the tool not turn on the dust collector
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
min_uptime = 5 #smallest amount of time the dust collector can be on for
dusty = Dust_collector('off', time.time(), min_uptime)  # create the dust collector
gatekeeper = Gate_manager()
tools['CloseAll'].status = "on"
tools['CloseAll'].flagged = True

if use_gui:
    gui_buttons = get_gui_buttons()



run = True


while run:

    if use_keyboard:
    # check the keyboard for input
        if use_keyboard == True:  # O
            key = curses.wrapper(key_getter)
            if key != -1:  # if nothing selected
                # prints: 'key: 97' for 'a' pressed
                print(f'\r                           key: {key} pressed')
                # '-1' on no presses
                keyboard_manager(key)
        time.sleep(.1)
    elif use_gui: #
        screen.fill(bg)
        for button in gui_buttons:
            if gui_buttons[button].draw_button():
                print(button)
        #counter_img = button_font.render(str(counter), True, red)
        #screen.blit(counter_img, (200, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


    # run through all the tools to see if they are on
    shop_manager()

    

pygame.quit()