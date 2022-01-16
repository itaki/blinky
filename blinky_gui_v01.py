import pygame
from pygame.locals import *
import curses # for keyboard
import time
import blinky_bits

#from os.path import dirname, join
#Get all the data to run the app
# create some list of shit I got
tools_file = 'tools.json'
gates_file = 'gates.json'
tools = blinky_bits.get_tools(tools_file)
gates = blinky_bits.get_gates(gates_file)
num_of_buttons = len(tools)

#set which interfaces to use
keyboard_present = True
use_gui = True

if use_gui:
    pygame.init()
    font = pygame.font.SysFont('Menlo', 6, bold=False)
    button_font = pygame.font.SysFont('Menlo', 10, bold=True)
    #font = pygame.font.Font('./fonts/Menlo', 6, bold=False)
    #button_font = pygame.font.Font('fonts/Menlo', 10, bold=True)
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

# define colours


# define global variable
clicked = False
counter = 0

def init():
    pass



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
    
    def __init__(self, x, y, text,):
        self.x = x
        self.y = y
        self.text = text
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
                if self.status == True:
                    self.hover_on()
                else: 
                    self.hover_off()
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
            if self.status == False:
                self.off()
            else: # status
                self.on()
        # add shading to button
        # pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        # pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        # pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        # pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = button_font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), self.y + 25))
        return action

def get_gui_buutons():
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



gui_buttons = get_gui_buutons()

print (gui_buttons)




run = True


while run:

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


pygame.quit()