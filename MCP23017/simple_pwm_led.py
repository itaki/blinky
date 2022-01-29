from time import sleep
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
from gpiozero import PWMLED


# this won't work until MCO23017 gets added to the gpiozero library
# https://github.com/gpiozero/gpiozero/pull/651
# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)  # MCP23017

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

# Now call the get_pin function to get an instance of a pin on the chip.
# This instance will act just like a digitalio.DigitalInOut class instance
# and has all the same properties and methods (except you can't set pull-down
# resistors, only pull-up!).  For the MCP23008 you specify a pin number from 0
# to 7 for the GP0...GP7 pins.  For the MCP23017 you specify a pin number from
# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
pin0 = PWMLED(mcp.get_pin(0))


# Setup pin0 as an output that's at a high logic level.
pin0.switch_to_output(value=True)

while True:
    # pin0.value = not pin1.value
    while True:
        pin0.value = 0  # off
        sleep(1)
        pin0.value = 0.5  # half brightness
        sleep(1)
        pin0.value = 1  # full brightness
        sleep(1)

