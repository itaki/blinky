from gpiozero import RGBLED, Button
from time import sleep

# btn1_led = RGBLED(21, 20, 19)
button1 = Button(18)


is_on = False
# btn1_led.on()

while True:
    if button1.when_released:
        if is_on == True:
            print("turning tool OFFFFFFF ")
            # btn1_led.off()
            is_on = False
    
        else:
            print("turning tool ON")
            # btn1_led.off()
            is_on = True
    
    
    
    # if button1.is_pressed:
    #     btn1_is = True
    # else:
    #     if btn1_is:
    #         if btn1_on:
    #             btn1_on = False
    #             print ("Button is off")
                
    #         else:
    #             btn1_on = True
    #             print ("button is on")
    #             btn1_led.on()
    #         btn1_is = False
    