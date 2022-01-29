import pygame


class Gui:
    '''Pygame object that manages the GUI'''
    def __init__(self, 
                width,
                height, 
                title, 
                gates_width, 
                consol_height, 
                columns_of_tools,
                theme):
        self.width = width
        self.height = height
        self.title = title
        