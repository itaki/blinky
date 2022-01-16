import time
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
chan1 = AnalogIn(ads, ADS.P1) #Curretnly using just P!


# Create single-ended input on channel 0
kit = ServoKit(channels=16)

cycles_to_average = 1000

while True:
    i = 0
    cycles = []
    while i < cycles_to_average:
        cycles.append(chan1.value)
        i = i+1
    po = np.mean(cycles)
    print(po)
    po_percent = po/24800
    set_range = po_percent *180
    if set_range > 180:
        set_range = 180
    if set_range < 0: 
        set_range = 0
    print(set_range)

    kit.servo[0].angle = set_range
    # time.sleep(0.5)