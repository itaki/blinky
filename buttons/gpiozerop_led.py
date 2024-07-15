from gpiozero import RGBLED, LED, Button
from signal import pause
import board
import busio
from adafruit_pca9685 import PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit

led =LED()
#led.color = (0, 1, 1)
ServoKit(channels=16, address = 0x40).servo[0]



# led.pulse(fade_in_time=1, fade_out_time=1, on_color=(1, 1, 1), off_color=(0, 0, 0), n=None, background=True)

pause()