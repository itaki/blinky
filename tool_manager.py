# tool manager
import curses
import keyboard # this library requires running the script as root
import time
import os, sys
import json
import questionary as q
import get_full_path
import blinky_bits as bb
import reorder_dict
from pathlib import Path
from adafruit_servokit import ServoKit
from gpiozero import LED, RGBLED, Button

from styles import custom_style_dope, get_styles

style = custom_style_dope

tools_file = 'tools.json'

class Tool:
    def __init__(self,
                 id_num,
                 name,
                 status,
                 override,
                 gate_prefs,
                 button_pin=0,
                 led_type='none',
                 r_pin=0,
                 g_pin=0,
                 b_pin=0,
                 voltage_pin=12,
                 amp_trigger=10,
                 keyboard_key=0,
                 last_used=0,
                 spin_down_time=5,
                 flagged=False):
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
        '''sets all the things when the toold is listed as ON'''
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