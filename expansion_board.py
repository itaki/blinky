import pstats
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

class Expansion_Board:
    def __init__(self, name, address, type, location) -> None:
        self.address = address

class Servo(Expansion_Board):
    pass

class 

servo_hat = ServoKit(channels=16, address  = 0x40)

