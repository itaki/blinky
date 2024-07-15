import board
import busio

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
    If the average value over ## cycles is above 1.66 then it is ON

    ADS1115 addresss can be 0x48 - 0x4B which is 72-74
    Pin numbers can be P0 - P3

    address wiring here
    https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring

    '''
    def __init__(self, voltage_address, trigger, sensor_not_detected = .8, min_readings = 6 ) -> None:
        self.address = voltage_address[0] # The voltage address comes in 2 parts. Board address
        self.pin_number = voltage_address[1] # and pin number
        self.trigger = trigger # value at which the plug is determined to be active
        self.sensor_not_detected = sensor_not_detected # value at which it doesn't see a sensor
        self.min_readings = min_readings
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
            print(f"ADS11x5 not found at {hex(self.address)}. Cannot create voltage sensor")


    def get_reading(self):
        '''gets a new reading and appends to readings list.
        if the list is full, removes the first reading in the list.
        returns the max value of the readings list'''
        self.reading = self.chan.voltage # get reading
        self.readings.append(self.reading) # append readings to readings list
        if len(self.readings) > self.min_readings:
            self.start = True
            self.readings.pop(0) # pop off the first reading to keep it tidy
        self.reading = max(self.readings) # Just hold onto the max reading
        return self.reading

    
    def am_i_on(self):
        '''answers the question of whether or not the plug has current being drawn from it'''
        self.get_reading()

        if self.start == True:
            if self.reading < self.sensor_not_detected: # if there is no sensor 
                if self.error_raised == False: 
                    self.error_raised = True #after error has been raised once, don't raise it again
                    print(f"It looks like there is a ADS1115 in location {hex(self.address)} but no AC715 on {self.pin_number}")
            elif self.reading < self.trigger: # if the tool is off return False
                self.error_raised = False # turn off the error raised because an AC715 has been added
                return False # since the tools is not on
            else: # the tools is ON!!! YEAH
                self.error_raised = False # turn off the error raised because an AC715 has been added
                return True # the tool is on