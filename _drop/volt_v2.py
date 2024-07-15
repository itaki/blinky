import time
import numpy as np
from statistics import mean
import board
import busio

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

#import module for board ads1115 - ADS because it's a constant
import adafruit_ads1x15.ads1115 as ADS

# The final import needed is for the ADS1x15 library's version of AnalogIn:
from adafruit_ads1x15.analog_in import AnalogIn

ads_48_pins = {'0' : ADS.P0, '1' : ADS.P1, '2' : ADS, '3' : ADS.P3}

# create the ADC object
ads_48 = ADS.ADS1115(i2c, address = 0x48)
ads_49 = ADS.ADS1115(i2c, address = 0x49)

pin0 = AnalogIn(ads_48, ADS.P0)
pin1 = AnalogIn(ads_48, ADS.P1)
pin2 = AnalogIn(ads_48, ADS.P2)
pin3 = AnalogIn(ads_48, ADS.P3)

while True:
    print(pin0.voltage, pin1.voltage, pin2.voltage, pin3.voltage)
    time.sleep(.25)


