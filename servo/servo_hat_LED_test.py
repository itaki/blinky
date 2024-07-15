#servo hat LED tests

import board
import busio
import digitalio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c_bus = busio.I2C(board.SCL, board.SDA)

led_hat = PCA9685(i2c_bus, address=0x40)


generic_servo = ServoKit(channels=16, address=0x43)
second_servo = ServoKit(channels=16, address=0x43)
# mcp = MCP23017(i2c_bus)  # MCP23017

led_hat.frequency = 1000

led_hat.channels[0].duty_cycle = 0xffff
led_hat.channels[1].duty_cycle = 0xffff
led_hat.channels[2].duty_cycle = 0xffff

running = True


while running:
    generic_servo.servo[15].angle = 50
    ServoKit(channels=16, address=0x40).servo[14].angle = 0
    led_hat.channels[0].duty_cycle = 0xffff
    led_hat.channels[1].duty_cycle = 0xffff
    led_hat.channels[2].duty_cycle = 0xffff

    for i in range(0xffff, 0x0000, -10):
        led_hat.channels[0].duty_cycle = i

    led_hat.channels[0].duty_cycle = 0xffff
    generic_servo.servo[15].angle = 90
    ServoKit(channels=16, address=0x43).servo[14].angle = 90

    for i in range(0xffff, 0x0000, -10):
        led_hat.channels[1].duty_cycle = i

    led_hat.channels[1].duty_cycle = 0xffff
    generic_servo.servo[15].angle = 130
    ServoKit(channels=16, address=0x43).servo[14].angle = 180

    for i in range(0xffff, 0x0000, -10):
        led_hat.channels[2].duty_cycle = i
    led_hat.channels[2].duty_cycle = 0xffff

    running = False
led_hat.deinit()



    


