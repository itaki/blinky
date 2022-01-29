from gpiozero import Button, LED
from signal import pause

def say_hello(button, text = ""):
    led25.on()
    print(text + str(button.pin.number))

def say_goodbye():
    print("Goodbye!")
    led25.off()

button1 = Button(27)
button2 = Button(21)
led25 = LED(25)

button1.when_pressed = say_hello
button1.when_released = say_goodbye
button2.when_pressed = say_hello
button2.when_released = say_goodbye

pause()