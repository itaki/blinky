from graphlib import TopologicalSorter


import blinky_bits
import pygame

# get the tools 
tools = blinky_bits.get_tools()
tools_with_v_snesor = {}
# get a list of the tools that have voltage sensor
for tool in tools:
    selected_tool = tools[tool]
    if selected_tool.voltage_address != []:
        tools_with_v_snesor[tool] = selected_tool

for tool in tools_with_v_snesor:
    print (tool)
# touchscree is 800x480
#initialize pygame
pygame.init()

# create the canvas
canvas_width = 480
canvas_height = 700
canvas = pygame.display.set_mode((canvas_width, canvas_height)) # double bracket because you have to deliver a tuple


number_of_sensors = len(tools_with_v_snesor)
padding = 10
total_padding = (number_of_sensors * padding) + padding

max_button_height = 50
button_height = canvas_height // number_of_sensors
if button_height > max_button_height:
    button_height = max_button_height

address_button_width = 50
set_button_width = 50
button_width = canvas_width - address_button_width - set_button_width

bg = '#16171d'
# Set the caption
pygame.display.set_caption('Voltage Sensor Setting')




# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        


