import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

use_voltage = True

# Create the ADC object using the I2C bus
if use_voltage:
    '''this activates the ADS1x15s and talks to the AC715s'''
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    start_address = 72 # ADS11x5s start at 72 or 0x48
    max_volt_meters = 4 # there can only be a max of 4 ADS1x15s 
    cycles = 0 # sets the number of cycles to 0
    review_cycles = 6 # number of cycles the voltage has to drop below the trigger to confirm the tool is off
    # ads=[]
    # for i in range(0, max_volt_meters):
    #     address = start_address+i
    #     ads[i] =
    #     try:
    #         ads0 = ADS.ADS1115(i2c, address = address)
    #         print(f"Adding ADS1115 at address {hex(address)} as {name}")
    #     except:
    #         print(f"No voltage contoller found at {hex(address)}")


# ads0 = ADS.ADS1115(i2c, address=0x48) # 48 is the one not on a board
address=0x48
# # amplify the signal
# ads0.gain = 1 # this will not affect the 
# Create single-ended input on channel 0
p_object = ADS.P0
chan0 = AnalogIn(ADS.ADS1115(i2c, address = address), p_object)

chan1 = AnalogIn(ADS.ADS1115(i2c, address = address), ADS.P1)
chan2 = AnalogIn(ADS.ADS1115(i2c, address = address), ADS.P2)
chan3 = AnalogIn(ADS.ADS1115(i2c, address = address), ADS.P3)

# ads1 = ADS.ADS1115(i2c, address=0x4A) # The othe one
# chan4 = AnalogIn(ads1, ADS.P0)
# chan5 = AnalogIn(ads1, ADS.P1)
# chan6 = AnalogIn(ads1, ADS.P2)
# chan7 = AnalogIn(ads1, ADS.P3)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    # print (f"chan0 : {chan0.value:>5} | chan1 : {chan1.value:>5} | chan2 : {chan2.value:>5} | chan3 : {chan3.value:>5} ")#| chan4 : {chan4.voltage:>1.4} | chan5 : {chan5.voltage:>1.4} | chan6 : {chan6.voltage:>1.4} | chan7 : {chan7.voltage:>1.4}")
    print (f"chan0 : {chan0.voltage:>1.4} | chan1 : {chan1.voltage:>1.4} | chan2 : {chan2.voltage:>1.4} | chan3 : {chan3.voltage:>1.4} ")#| chan4 : {chan4.voltage:>1.4} | chan5 : {chan5.voltage:>1.4} | chan6 : {chan6.voltage:>1.4} | chan7 : {chan7.voltage:>1.4}")
    # print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    # print("{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    # print("{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
    time.sleep(0.5)