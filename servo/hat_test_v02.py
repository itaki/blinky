
# from adafruit_servokit import ServoKit
# kit = ServoKit(channels=16)


# kit.servo[0].angle = 62

import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)


kit.continuous_servo[1].throttle = .2
time.sleep(4)
kit.continuous_servo[1].throttle = .2
time.sleep(4)

kit.continuous_servo[1].throttle = 0