import board
import busio
import adafruit_ads1x15.ads1115 as ADS

i2c = busio.I2C(board.SCL, board.SDA)
address_as_int = 72
address_as_hex = hex(address_as_int)
print (address_as_hex) # returns 0x48 like it's suppose to
try:
    ads0 = ADS.ADS1115(i2c, address = hex(address_as_hex)) # Errors out
except:
    print(f"Didn't find a device on {address_as_hex}") # "Didn't find a device on 0x48"
# but running this
ads0 = ADS.ADS1115(i2c, address = 0x48) # finds my device.
