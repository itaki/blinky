from gpiozero import LED, Button
from time import sleep

btn1_led = LED(18)
button1 = Button(27)
btn1_is = False
btn1_on = False



while True:
    if button1.is_pressed:
        btn1_is = True
    else:
        if btn1_is:
            if btn1_on:
                btn1_on = False
                print ("Button is off")
            else:
                btn1_on = True
                print ("button is on")
            btn1_is = False
