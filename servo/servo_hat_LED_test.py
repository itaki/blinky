#servo hat LED tests

import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
servo_hat = ServoKit(channels=16)

i2c_bus = busio.I2C(board.SCL, board.SDA)
#servo_hat = PCA9685(i2c_bus, address=0x40)
led_hat = PCA9685(i2c_bus, address=0x41)

led_hat.frequency = 60
led_channel = led_hat.channels[0] # this is an attibute and the index is 15
led_channel.duty_cycle = 0xffff

servo_hat.servo[0].angle = 130
