import os, sys
import json
import get_full_path
import time
import blinky_bits as bb
import reorder_dict
from pathlib import Path
from gpiozero import PWMLED, RGBLED, Button, OutputDevice
import voltage_sensor, buttons, leds
import board
import busio
import json
import os
import get_full_path
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)

# Specify the tools_file and backup directory 
# These will be sent from main, but are also placed here for running this

TOOLS_FILE = 'tools.json'
BACKUP_DIR = '_BU'
on_led_color = 0xffff
spindown_led_color = 0x8888
off_led_color = 0x1111
on_rgb_color = {'bright' : (.51, .9, 0), 'dark' : (.6, 1, .1)}
spindown_rgb_color = {'bright' : (1, .59 , 0), 'dark' : (0, 0, 0)}
off_rgb_color = {'bright' : (.1, .82, .90), 'dark' : (.1, .82, .90)}

class Tool:
    ''' Tool class that holds all the variables associated to the tool 
        as well as the button objects and gate_prefs dictionary
        
        Variables:
        id_num : don't think this is used since dictionaries can now be ordered
        name : name of the tool
        status : on, off, spindown
        override : bool - if turned on in pygame, it overrides the tool setting. Note that it won't override the tool to off
        gate_prefs : list of gates that the tool wants open
        button_pin : int GPIO pin that the button is on. If -1 then no button is assigned to it
        led_type : 'RGB' or 'LED' if there is a button, specify what kind of led it has
        r_pin : red led pin, or for single led, the pin associated with it
        g_pin : green led pin
        b_pin : blue led pin
        voltage_sensor : infomation about the voltage sensor 
        keyboard_key : the specified key that relates to a tool 
        last_used : the time the tool was last "on". used to determine if it has spun down long enough
        spin_down_time : time in seconds for the tool to keep the dust collector on before not needing it anymore
        
        Methods:
        create_button : if not -1 then creates a button object on the pin
        button_cycle : if button was just on, turn it off. if 
        create_led : if button exists and led pin is not -1 then creates an led_type on pin or pins
        turn_on : set all the all funtions of the tool including led color
        '''
    def __init__(self, tool):
        self.tool_dict = tool
        self.pins_used = []
        self.id_num = tool['id_num']
        self.name = tool['name']
        self.status = 'off'
        self.override = False
        self.gate_prefs = tool['gate_prefs']
        if tool['button'] != {}:
            self.create_button(tool['button'])
            self.pins_used.append(tool['button']['pin'])

        if tool['led'] != {}:
            self.create_led(tool['led'])
            if tool['led']['type'] == 'PWMLED':
                self.pins_used.append(tool['led']['pin'])
            elif tool['led']['type'] == 'RGB':
                self.pins_used.extend(tool['led']['pins'])

        if tool['volt'] != {}:
            self.voltage_sensor = voltage_sensor.Voltage_sensor(tool['volt'])

        self.keyboard_key = tool['keyboard_key']       
        self.spin_down_time = tool['spin_down_time']
        self.last_used = 0
        self.flagged = False


            
    def create_button(self, btn_dict):
        '''Create a physical connection to a button'''
        print(f"Creating {self.name} button at address {btn_dict['address']} on pin {btn_dict['pin']}")
        if btn_dict['address'] == 'pi': # a button that is not directly attached to the pi
            self.btn = Button(btn_dict['pin'])
            self.btn.when_pressed = self.button_cycle
            print(f"{self.name} button pressed")
        else:
            print('Buttons not directly connected to pi are not supported right now')
            #self.btn = buttons.Non_Standard_Button(btn_dict) # this needs to be developed for buttons not directly connected to the pi
           
            
    def create_led(self, led_dict):
        
        if led_dict['address'] == 'pi':
               
            if led_dict['type'] == "RGB":
                self.led = RGBLED(led_dict['pins'][0], led_dict['pins'][1], led_dict['pins'][2])
                self.led_type = "RGB"
                print(f"created RGBLED on {led_dict['pins'][0], led_dict['pins'][1], led_dict['pins'][2]}")
            
            elif led_dict['type'] == "PWMLED":
                self.led = PWMLED(led_dict['pin'], initial_value=0)
                self.led_type = "PWMLED"
                print(f"Creating an {led_dict['type']} LED on {led_dict['address']} on pin {led_dict['pin']}")
            
            elif led_dict['type'] == "RELAY":
                self.led = OutputDevice(led_dict['pin'], initial_value=False)
                self.led_type = "RELAY"
            
            else:
                print(f"no led created for {self.name}")
        else:
            print('LEDs not directly connected to pi are not supported right now')

    def button_cycle(self):
        '''this runs when a real hard button is pressed. It overrides the voltage'''
        if self.status == 'on':
            self.override = False
            print(f"Override for {self.name} OFF")
            self.spindown()
        else:
            self.override = True
            print(f"Override engaged for {self.name}")
            self.turn_on()

    def turn_on(self):
        self.status = 'on'
        self.flagged = True
        if hasattr(self, "led"):
            if self.led_type == "RGB":
                self.led.pulse(fade_in_time=1, fade_out_time=1, on_color=(.51, .9, 0), off_color=(.6, 1, .1), n=None, background=True)
            elif self.led_type == "PWMLED":
                self.led.on()
            elif self.led_type == "RELAY":
                self.led.on()
        print(f'----------->{self.name} turned ON')

    def spindown(self):
        self.status = 'spindown'
        self.last_used = time.time()
        if hasattr(self, "led"):
            if self.led_type == "RGB":
                self.led.pulse(fade_in_time=1, fade_out_time=1, on_color=(1, .59 , 0), off_color=(0, 0, 0), n=None, background=True)
            elif self.led_type == "PWMLED":
                self.led.pulse(fade_in_time=1, fade_out_time=1, n=None, background=True)
            elif self.led_type == "RELAY":
                #self.led.on()
                pass
        print(f'----------->{self.name} set to SPINDOWN for {self.spin_down_time}')

    def turn_off(self):
        self.status = 'off'
        self.flagged = True
        if hasattr(self, "led"):
            if self.led_type == "RGB":
                self.led.color = (.1, .82, .90)
            elif self.led_type == "PWMLED":
                self.led.value = .5
            elif self.led_type == "RELAY":
                self.led.off()

        print(f'----------->{self.name} turned OFF')

class LED:
    def __init__(self,
                address,
                pin
                ):
        self.led = LED(pin)
        self.on_color = on_led_color
        self.spindown_color = spindown_led_color
        self.off_color = off_led_color
    def turn_on(self):
        self.led.on # maybe later do a color value
    def turn_off(self):
        self.led.off
    def spindown(self):
        self.led.blink(on_time = 1, off_time = 1, n=None, background=True) #maybe late do a brightness value or if PWM I can pulse
    
class RGB:
    def __init__(self,
                r_pin,
                g_pin,
                b_pin
                ):
        self.led = RGBLED(r_pin, g_pin, b_pin)
        self.r_pin = r_pin #don't think I need this
        self.g_pin = g_pin #don't think I need this
        self.b_pin = b_pin #don't think I need this
        self.on_color = on_rgb_color
        self.spindown_color = spindown_rgb_color
        self.off_color = off_rgb_color
    def turn_on(self):
        self.led.pulse(fade_in_time = 1, 
                        fade_out_time = 1, 
                        on_color = self.on_color['bright'], 
                        off_color = self.on_color['dark'], 
                        n = None, 
                        background = True)
        self.led.pulse(fade_in_time = 1, 
                        fade_out_time = 1, 
                        on_color = self.spindown_color['bright'], 
                        off_color = self.spindown_color['dark'], 
                        n = None, 
                        background = True)
    def turn_off(self):
        self.led.color = self.off_color('bright')

class Tool_Manager:
    def __init__(self, tools_file = "tools.json", backup_dir = "_BU") -> None:
        self.get_tools(tools_file)
        self.backup_dir = backup_dir

    def get_tools(self, file):
        tools_list = []
        tools = {}
            # LOAD ALL THE TOOLS
        if os.path.exists(file): # if there is a tools file load it
            file_path = get_full_path.path(file)  # set the file path
            with open(file_path, 'r') as f:  # read the tool list
                tools_list = json.load(f)  # load tool list into python

            for tool in tools_list:
                tools[tool['name']] = Tool(tool) #build all the tools
                # 1print(tool)
        self.tools = tools
    #print(f'These are your tools {tools}')

    def get_used_pins(self):
        all_used_pins = []
        for tool in self.tools:
            selected_tool = self.tools[tool]
            all_used_pins.extend(selected_tool.pins_used)
            
        return all_used_pins

    def whats_on_pin(self, pin):
        for tool in self.tools:
            selected_tool = self.tools[tool]
            if pin in selected_tool.pins_used:
                return selected_tool.name
            
        return "No Tool"




if __name__ == '__main__':
    tm = Tool_Manager(TOOLS_FILE, BACKUP_DIR)
    pins_in_use = tm.get_used_pins()
    pins_in_use.sort()
    print (f"{pins_in_use}")