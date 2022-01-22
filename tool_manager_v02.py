import os, sys
import json
import get_full_path
import time
import blinky_bits as bb
import reorder_dict
from pathlib import Path
from gpiozero import LED, RGBLED, Button

# Specify the tools_file and backup directory 
# These will be sent from main, but are also placed here for running this

gates_file = 'tools.json'
backup_dir = '_BU'
on_led_color = 255
spindown_led_color = 128
off_led_color = 10
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
        voltage_pin : if there is a voltage drop sensor, the pin that it is on. -1 for no sensor
        amp_trigger : the trigger point that the voltage sensor says the tool is on 
        keyboard_key : the specified key that relates to a tool 
        last_used : the time the tool was last "on". used to determine if it has spun down long enough
        spin_down_time : time in seconds for the tool to keep the dust collector on before not needing it anymore
        
        Methods:
        create_button : if not -1 then creates a button object on the pin
        button_cycle : if button was just on, turn it off. if 
        create_led : if button exists and led pin is not -1 then creates an led_type on pin or pins
        turn_on : set all the all funtions of the tool including led color
        '''
    def __init__(self,
                 id_num = int,
                 name = str,
                 status = str('off'),
                 override = bool(False),
                 gate_prefs = [],
                 button_pin = int(-1), # if -1 then tool does NOT have a button associated with it
                 led_type = 'none', 
                 r_pin = -1,
                 g_pin = -1,
                 b_pin = -1,
                 voltage_pin = -1,
                 amp_trigger = 20,
                 keyboard_key = 0,
                 last_used = 0,
                 spin_down_time = 5,
                 flagged = False):
        self.id_num = id_num
        self.name = name
        self.status = status
        self.override = override
        self.gate_prefs = gate_prefs
        self.button_pin = button_pin
        self.led_type = led_type
        self.r_pin = r_pin
        self.g_pin = g_pin
        self.b_pin = b_pin
        self.voltage_pin = voltage_pin
        self.amp_trigger = amp_trigger
        self.keyboard_key = keyboard_key
        self.last_used = last_used
        self.spin_down_time = spin_down_time
        self.flagged = flagged

        if self.button_pin > 0: # 0 or -1 means no button
            print(f"Creating {self.name} on {self.button_pin}")
            self.create_button()
            if self.led_type != 'none':
                self.create_led()
            # create a button object and put it in the dictionary
            
    def create_button(self):
        '''Create a physical connection to a button'''
        self.btn = Button(self.button_pin)
        self.btn.when_pressed = self.button_cycle
        if self.led_type != 'none':
            self.create_led
            
    def create_led(self):
        print(f"led type = {self.led_type}")
        if self.led_type == "RGB":
            self.led = RGB_highlight(self.r_pin)


            self.led = RGBLED(self.r_pin, self.g_pin, self.b_pin)
            print(f"created RGBLED on {self.r_pin, self.g_pin, self.b_pin}")
            self.led.color = (1,1,1)
        elif self.led_type == "LED":
            self.led = LED(self.r_pin)
            print(f"created LED on {self.r_pin}")
        else:
            print(f"no button created for {self.name}")

    def button_cycle(self):
        '''this runs when a real hard button is pressed. It overrides the voltage'''
        if self.status == 'on':
            self.override = False
            print(f"Override OFF")
            self.spindown()
        else:
            self.override = True
            print(f"Override engaged because {self.name} is on")
            self.turn_on()

    def turn_on(self):
        self.status = 'on'
        self.flagged = True
        if self.button_pin != 0:
            if self.led_type == "RGB":
                self.led.pulse(fade_in_time=1, fade_out_time=1, on_color=(.51, .9, 0), off_color=(.6, 1, .1), n=None, background=True)
            elif self.led_type == "LED":
                self.led.on
        print(f'----------->{self.name} turned ON')

    def spindown(self):
        self.status = 'spindown'
        self.last_used = time.time()
        if self.button_pin != 0:
            if self.led_type == "RGB":
                self.led.pulse(fade_in_time=1, fade_out_time=1, on_color=(1, .59 , 0), off_color=(0, 0, 0), n=None, background=True)
            elif self.led_type == "LED":
                self.led.off
        print(f'----------->{self.name} set to SPINDOWN for {self.spin_down_time}')

    def turn_off(self):
        self.status = 'off'
        self.flagged = True
        if self.button_pin != 0:
            if self.led_type == "RGB":
                self.led.color = (.1, .82, .90)
            elif self.led_type == "LED":
                self.led.off
        print(f'----------->{self.name} turned OFF')

class Button_LED:
    def __init__(self,
                pin = -1,
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
    
class Button_RGB:
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

class Tool_manager:
    def __init__(self) -> None:
        pass

