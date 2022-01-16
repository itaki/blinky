from gpiozero import LED, RGBLED, Button
from signal import pause
import blinky_bits
tools = blinky_bits.get_tools('tools.json')

class Create_button():
    def __init__(self,tool):
        print(tool)
        button_pin = tool.button_pin
        led_type = tool.led_type
        r_pin = tool.r_pin
        g_pin = tool.g_pin
        b_pin = tool.b_pin
        status = tool.status
        self.create_button(led_type, r_pin, g_pin, b_pin)
        
    
    def pressed(self):
        if self.status == 'on':
            self.status = 'spindown' 
            self.led.color = (1, 1, 0)
        elif self.status == 'spindown':
            self.status = 'on'
            self.led.color = (1, 0, 0)
        elif self.status == 'off':
            self.status = 'on'
            self.led.color = (0, 1, 1)
    
    def create_button(self, led_type, r_pin, g_pin, b_pin):
        self.btn = Button(self.button_pin)
        print(led_type, r_pin, g_pin, b_pin)
        if led_type == "RGB":
            self.led = RGBLED(r_pin, g_pin, b_pin)
            print(f"created LED on {r_pin, g_pin, b_pin}")
            self.led.color(1,1,1)
        elif led_type == "LED":
            self.led = LED(r_pin)
        else:
            print(f"no button created for {self.name}")



    





def say_hello(pin):
    print(pin)
    for tool in tools:
        current_tool = tools[tool]
        if pin == current_tool.button_pin:
            print(f"just pressed the {current_tool.name} button")


def say_goodbye():
    print("Goodbye!")


for tool in tools:
    # select the tool I'm currently working with
    current_tool = tools[tool]
    if current_tool.button_pin != 0:
        print(f"Creating {current_tool.name} on {current_tool.button_pin}")
        # create a button object and put it in the dictionary
        current_tool.btn = Button(current_tool.button_pin)
        current_tool.btn.when_pressed = current_tool.button_cycle
        current_tool.btn.when_released = say_goodbye


# current_tool = tools['TableSaw']

# btn = Button(current_tool.button_pin)
# btn.when_pressed = say_hello
# btn.when_released = say_goodbye

pause()