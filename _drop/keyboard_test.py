import keyboard
import time

while True: #   
    try:
        if keyboard.is_pressed('q'): #
            print("you pressed q")
    except:
        print("no key")
    currenttime = time.time()
    print (f'the new time is {currenttime}' )
    time.sleep(1)
