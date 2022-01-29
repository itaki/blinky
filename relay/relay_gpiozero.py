import gpiozero

from gpiozero import Button, LED, OutputDevice
from signal import pause



def say_hello(button, text = ""):
    led25.on()
    relay.on()
    print(text + str(button.pin.number))

def say_goodbye():
    print("Goodbye!")
    relay.off()
    led25.off()

button1 = Button(27)

relay = OutputDevice(21)
led25 = LED(25)

button1.when_pressed = say_hello
button1.when_released = say_goodbye

pause()
