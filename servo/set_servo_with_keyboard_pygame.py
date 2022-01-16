#set servo with keyboard

import pygame
import sys
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_servokit import ServoKit
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)
#chan1 = AnalogIn(ads, ADS.P1) #Curretnly using just P!


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
