import time
#https://forums.raspberrypi.com/viewtopic.php?f=63&t=221972&hilit=acs712&start=150#p1366441
#pip install Adafruit-ADS1x15

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

def   ConversionToAmp(values):
   return ((values * 2.048/32767)-1.25) * 1000.0/33.0
   
GAIN = 2
try:

  while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        if i==0:
           values[i] = ConversionToAmp(adc.read_adc(i, gain=GAIN, data_rate=128))
        else:
           values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
    time.sleep(0.5)
    print("0:{0:2.1f}A\t1:{1:5}\t2:{2:5}\t3:{3:5}".format(*values))

except KeyboardInterrupt:
   pass