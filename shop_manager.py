import json
import time
import get_full_path
from datetime import datetime
import questionary as q
import shutil #allows for copying a file to make a backup
import os
from styles import custom_style_dope
import blinky_bits as bb
import errno
from adafruit_servokit import ServoKit
from gpiozero import LED, RGBLED, Button
import blinky_bits
kit = ServoKit(channels=16)

#style the questions
style = custom_style_dope
gates_file = 'gates.json'
tools_file = 'tools.json'
backup_directory = '_BU'
force_backup = True


if __name__ == "__main__":
    tools = bb.get_tools('tools.json')
    gates = bb.get_gates('gates.json')
    print (len(gates))
    print (tools['TableSaw'].name)
    