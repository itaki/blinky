import time
import numpy as np
from statistics import mean
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
# import adafruit_ads1x15.ads1115
from adafruit_ads1x15.analog_in import AnalogIn
from pkg_resources import PEP440Warning

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
off_below = 1.7

class Voltage_sensor:
    '''
    Given an ADS1115 address and a corresponding pin number 
    will read voltage values from an ACS715

    If value is below .65 there is no AC715 attached to the pin
    If value is below 1.656 or a little higher, it is OFF
    If the average value over 6 cycles is above 1.66 then it is ON

    ADS1115 addresss can be 0x48 - 0x4B which is 72-74
    Pin numbers can be P0 - P3

    address wiring here
    https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring

    '''
    def __init__(self, address, pin_number, trigger) -> None:
        self.address = int(address, 0) # 0 because need to specify that it is hex comming in
        self.pin_number = pin_number
        self.trigger = trigger
        self.no_sensor = 1
        self.readings_for_check = 20
        self.readings = []
        self.error_raised = False
        self.start = False
        self.pins = {'0' : ADS.P0, '1' : ADS.P1, '2' : ADS.P2, '3' : ADS.P3}
        try:
            #self.chan = AnalogIn(adafruit_ads1x15.ads1115.ADS1115(i2c, address = self.address), adafruit_ads1x15.ads1115.P0) 
            self.chan = AnalogIn(ADS.ADS1115(i2c, address = self.address), self.pins[str(self.pin_number)])
            print(f"Adding ADS1115 at address {hex(self.address)}")
            self.am_i_on()
        except:
            print(f"Voltage Sensor not found at {hex(self.address)}")

    def get_reading(self):
        self.reading = self.chan.voltage # get reading
        self.readings.append(self.reading) # append readings to readings list
        if len(self.readings) > self.readings_for_check:
            self.start = True
            self.readings.pop(0) # pop off the first reading to keep it tidy
        self.reading = max(self.readings)

    
    def am_i_on(self):
        self.get_reading()

        if self.start == True:
  
            if self.reading < self.no_sensor: # if there is no sensor 
                if self.error_raised == False:
                    self.error_raised = True
                    print(f"It looks like there is a ADS1115 in location {hex(self.address)} but no AC715 on {self.pin_number}")
                return False
            elif self.reading < self.trigger: # if the tool is off return False
                self.error_raised = False # turn off the error raised because an AC715 has been added
                return False
            else: # the tools is ON!!! YEAH
                self.error_raised = False # turn off the error raised because an AC715 has been added
                return True

    
if __name__=="__main__":
    address = "0x48"
    pin_number = 0
    trigger = 1.658
    voltage_sensor = Voltage_sensor(address, pin_number, trigger)
    is_it_on = False

    while True:
        if voltage_sensor.am_i_on() == True and is_it_on == False:
            print(f"\rVoltage Sensor at {hex(voltage_sensor.address)} and pin {voltage_sensor.pin_number} is on and reading {voltage_sensor.reading}" )
            is_it_on = True
        elif voltage_sensor.am_i_on() == False and is_it_on ==True:
            print(f"\rAverage reading {voltage_sensor.reading}")
            is_it_on = False

        # time.sleep(.5)


