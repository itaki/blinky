import time
import numpy as np
from statistics import mean
import board
import busio
import tool_manager
from _drop.volt import Voltage_sensor
import pygame



# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

#import module for board ads1115 - ADS because it's a constant
import adafruit_ads1x15.ads1115 as ADS

# The final import needed is for the ADS1x15 library's version of AnalogIn:
from adafruit_ads1x15.analog_in import AnalogIn
# AnalogIn is the main object. I'll create a bunch of AnalogIn's and be able to read them just by asking for the objects voltage

#ads_pin_numbers = {'0' : ADS.P0, '1' : ADS.P1, '2' : ADS.P2, '3' : ADS.P3}
#possible_addresses = (0x48, 0x49, 0x4A, 0x4B)

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
    def __init__(self, voltage_address, trigger) -> None:
        self.address = voltage_address[0]
        self.pin_number = voltage_address[1]
        self.trigger = trigger
        self.no_sensor = 1 # value at which it doesn't see a sensor
        self.readings_for_check = 6
        self.readings = []
        self.error_raised = False
        self.start = False
        self.was_i_on = False
        try:
            #self.chan = AnalogIn(adafruit_ads1x15.ads1115.ADS1115(i2c, address = self.address), adafruit_ads1x15.ads1115.P0) 
            self.chan = AnalogIn(ADS.ADS1115(i2c, address = self.address), self.pin_number)
            print(f"Adding ADS1115 at address {hex(self.address)}")
            print(f"Current voltage reading is {self.chan.voltage}")
            self.am_i_on()
        except:
            print(f"Voltage Sensor not found at {hex(self.address)}. Cannot create voltage sensor")


    def get_reading(self):
        self.reading = self.chan.voltage # get reading
        self.readings.append(self.reading) # append readings to readings list
        if len(self.readings) > self.readings_for_check:
            self.start = True
            self.readings.pop(0) # pop off the first reading to keep it tidy
        self.reading = max(self.readings) # Just hold onto the max reading
        return self.reading

    
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
                return False # since the tools is not on
            else: # the tools is ON!!! YEAH
                self.error_raised = False # turn off the error raised because an AC715 has been added
                return True # the tool is on


class Tool:
    def __init__(self, name, voltage_address, trigger):
        self.name = name
        self.voltage_address = voltage_address
        self.trigger = trigger
        self.voltage_sensor = Voltage_sensor(self.voltage_address, self.trigger)

def show_all_tools_status(tools_list):
    freshenup = True
    for tool in tools_list:
        if freshenup == True:
            print('')
            freshenup = False
        voltage_reading = tool.voltage_sensor.get_reading()
        tool_status = tool.voltage_sensor.am_i_on()
        print (f"{tool.name} {voltage_reading:.8f} {tool_status}   -   ", end="")

mitersaw = Tool(name = 'mitersaw', voltage_address = (0x48, ADS.P0), trigger = 1.6)
tablesaw = Tool(name = 'tablesaw', voltage_address = (0x48, ADS.P1), trigger = 1.6)
bandsaw = Tool(name = 'bandsaw', voltage_address = (0x48, ADS.P2), trigger = 1.6)
drillpress = Tool(name = 'drillpress', voltage_address = (0x48, ADS.P3), trigger = 1.6)
tools_list = [mitersaw, tablesaw, bandsaw, drillpress]
# create the ADC object
#ads_48 = ADS.ADS1115(i2c, address = 0x48)

class Address:
    '''Creates a heading for the address block'''
    def __init__(self, address):


gui = True
if gui:
    pygame.init()
    width = 600
    height = 400
    padding = 10
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('set voltage ')



while True:
    if gui:
        pass
    else:
        show_all_tools_status(tools_list)
        time.sleep(.5)

