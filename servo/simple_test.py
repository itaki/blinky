# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio
import time

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus, address = 0x48) 

# 50 is table saw 
# 40 is main board

# Set the PWM frequency to 60hz.
pca.frequency = 1000

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.




# pca.channels[1].angle = 90
# pca.channels[7].angle = 70
# pca.channels[11].angle = 70
# pca.channels[15].angle = 70

# pca.channels[1].angle = 150
# pca.channels[7].angle = 150
# pca.channels[11].angle = 150
# pca.channels[15].angle = 150

while True:
    for angle in range (30, 80):
        for c in range(0,15):
            pca.channels[c].angle = angle
        print(f'moved angle up to {angle}')
        time.sleep(.05)
            
    for angle in range (80, 30,-1):
        for c in range(0,15):
            pca.channels[c].angle = angle
        print(f'moved angle up to {angle}')
        time.sleep(.05)