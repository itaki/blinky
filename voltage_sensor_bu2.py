import os, sys
import json
import get_full_path
import board
import busio
import time


# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

#import module for board ads1115 - ADS because it's a constant
import adafruit_ads1x15.ads1115 as ADS

# The final import needed is for the ADS1x15 library's version of AnalogIn:
from adafruit_ads1x15.analog_in import AnalogIn
# AnalogIn is the main object. I'll create a bunch of AnalogIn's and be able to read them just by asking for the objects voltage

ads_pin_numbers = {0 : ADS.P0, 1 : ADS.P1, 2 : ADS.P2, 3 : ADS.P3}
#possible_addresses = (0x48, 0x49, 0x4A, 0x4B)



class Voltage_sensor:
    '''
    Given an ADS1115 address and a corresponding pin number 
    will read voltage values from an ACS712

    If value is below .65 there is no AC712 attached to the pin
    If value is below 1.656 or a little higher, it is OFF
    If the average value over ## cycles is above 1.66 then it is ON

    ADS1115 addresss can be 0x48 - 0x4B which is 72-74
    Pin numbers can be P0 - P3

    address wiring here
    https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring

    '''
    def __init__(self, volt, sensor_detection_threshhold = 1.6, trigger = 1.09, min_readings = 10 ) -> None:
        self.board_address = volt['voltage_address']['board_address'] # The voltage address comes in 2 parts. Board address
        self.pin_number = ads_pin_numbers[volt['voltage_address']['pin']] # and pin number
        self.sensor_detection_threshhold = sensor_detection_threshhold # value at which it doesn't see a sensor
        self.sensor_exists = True # this gets set to false if 
        self.trigger = trigger
        self.min_readings = min_readings
        self.readings = []
        self.error_raised = False
        self.board_exists = None
        try:
            self.chan = AnalogIn(ADS.ADS1115(i2c, address = self.board_address), self.pin_number)
            self.board_exists = True
            print(f"⚡⚡⚡⚡⚡⚡⚡⚡ Adding Voltage Sensor on pin {self.pin_number} on ADS1115 at address {hex(self.board_address)}")
            reading = self.get_reading()
            print(f"        Current voltage reading is {reading}")
            self.set_trigger_voltage()
        except:
            print(f"■■■■■ ERROR! ■■■■■■  ADS11x5 not found at {hex(self.board_address)}. Cannot create voltage sensor")
            self.board_exists = False

    def set_trigger_voltage(self):
        reading = self.get_reading()   
        if self.in_good_range():
            self.trigger = reading * self.trigger
            print (f"Setting trigger point on pin {self.pin_number} at address {hex(self.board_address)} to {self.trigger}")

    def get_reading(self):
        '''gets a new reading and appends to readings list.
        if the list is full, removes the first reading in the list.
        returns the max value of the readings list'''
        if self.board_exists:
            try:
                reading = self.chan.voltage # get reading
                self.readings.append(reading) # append readings to readings list
                if len(self.readings) <= self.min_readings: # Make sure the list of readings has enough readings
                    self.get_reading()
                else:      
                    self.readings.pop(0) # pop off the first reading to keep it tidy
                max_reading = max(self.readings) # Just hold onto the max reading
                self.reading = max_reading
                return max_reading
            except:
                print(f"ERROR GETTING READING FROM {self.board_address} at PIN {self.pin_number}")
                return self.reading
        else:
            return 0

    def in_good_range(self):
        '''Checks to see if the reading is in a good range'''

        if self.sensor_detection_threshhold < self.reading:
            self.error_raised = False
            self.sensor_exists = True
            return True
        elif self.error_raised == False:
            self.error_raised = True
            if self.sensor_detection_threshhold > self.reading:
                pass
                #print (f"⛔⛔⛔⛔ CAUTION!!!!!   It looks as though there is no sensor on pin {self.pin_number} at address {hex(self.board_address)} ")
        self.sensor_exists = False
        return False

    def am_i_on(self):
        '''This is the main method of this class
        answers the question of whether or not the plug has current being drawn from it'''
        # If the ADS1115 was never found, it was never created, so skip this entirely 
        if self.board_exists:
            reading = self.get_reading()
            if self.in_good_range() and self.sensor_exists:
                if reading > self.trigger: # I am on
                    #print(reading)
                    return True
                else:
                    return False # I am not on

            else: # there is no sensor
                if self.in_good_range():
                    self.set_trigger_voltage() 
                    self.am_i_on()
                else:

                    return False
        else:
            return False

    



def show_all_tools_status(tools_list):
    freshenup = True
    for tool in tools_list:
        selcted_tool = tools_list[tool]
        if freshenup == True:
            print('')
            freshenup = False
        voltage_reading = selcted_tool.voltage_sensor.get_reading()
        tool_status = selcted_tool.voltage_sensor.am_i_on()
        print (f"{selcted_tool.name} {voltage_reading:.8f} {tool_status}   -   ", end="")

def get_tools_with_sensor(tools):
    '''takes a list of tools and returns a list of names of tools that have a voltage sensor attached'''
    tools_with_v_sensor = []
    for tool in tools:
        selected_tool = tools[tool]
        if hasattr(selected_tool, 'voltage_sensor'):
            tools_with_v_sensor.append( selected_tool.name)
    return tools_with_v_sensor


if __name__ == "__main__":
    pass



