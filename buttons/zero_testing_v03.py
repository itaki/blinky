from gpiozero import Button
from signal import pause
button21_is_on = False




def say_hello(btn_no):
    button_name = f"button{btn_no}_is_on"
    if button_name == True:
        button_name = False
        print("Turning off")
    else:
        button_name = True
        print("Turning off")

def say_goodbye():
    print("Goodbye!")

button = Button(27)

button.when_pressed = say_hello(27)
button.when_released = say_goodbye

i=0

pause()