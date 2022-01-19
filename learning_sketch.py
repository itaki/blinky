#https://www.youtube.com/watch?v=a5JWrd7Y_14&ab_channel=CDcodes
from re import T
import pygame

class Shotbot():
    def __inti__(self):
        pygame.init()
        self.running, self.gate_settings, self.tool_settings = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY - False, False, False, False

        self.DISPLAY_W, self.DISPLAY_H = 720,480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = 'fonts/Menlo Regular.ttf'
        self.BACKGROUND, self.TEXT = (22, 23, 29), (129, 249, 0)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.gate_settings, self.tool_settings = False, False, False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                