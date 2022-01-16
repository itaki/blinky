#set servo with keyboard

import pygame
import sys

from adafruit_servokit import ServoKit


# Create single-ended input on channel 0
kit = ServoKit(channels=16)


pygame.init()
#create canvas
display = pygame.display.set_mode((300, 300))

set_range = 90 #set the servo in the middle
adjustment = 0

while True:
    # check the keyboard for input4
    # creating a loop to check events that
    # are occuring
    adjustment = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                adjustment = -1
            if event.key == pygame.K_LEFT:
                adjustment = -10
            if event.key == pygame.K_UP:
                adjustment = 1
            if event.key == pygame.K_RIGHT:
                adjustment = 10
            if event.key == pygame.K_0:
                set_range = 89
                adjustment = 1
            if adjustment != 0:
                set_range = set_range + adjustment
                  
                if set_range > 180:
                    print("TOO HIGH!!!!!!")
                    set_range = 180
                if set_range < 0: 
                    print("TOO LOW!!!!!")
                    set_range = 0
                
                print(f"Angle = {set_range}")
                kit.servo[0].angle = set_range
