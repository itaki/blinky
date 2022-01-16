from gpiozero import Servo
from time import sleep

servo = Servo(17)

while True:
    servo.mid()
    print('mid')
    sleep(0.5)
    servo.min()
    print('min')
    sleep(0.5)
    servo.mid()
    print('mid')
    sleep(0.5)
    servo.max()
    print('max')
    sleep(0.5)
