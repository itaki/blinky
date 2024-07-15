from gpiozero import LED, Button

led = LED(18)
button = Button(23)

def release_happened():
    print("was released")

while True:
    test = button.is_pressed
    print (test)