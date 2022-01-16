import keyboard
import time
import json
import tkinter as tk
from os.path import dirname, join

#get the tool file
current_dir = dirname(__file__)
file_path = join(current_dir, "./tools.json")
with open(file_path, 'r') as tools_list:
	tools = json.load(tools_list)
dump = json.dumps(tools, indent=4)
print(dump)

while True:
    pressed = keyboard.is_pressed()
    print(f'this key was pressed {pressed}')


# while True: #   
#     try:
#         if keyboard.is_pressed('q'): #
#             print("you pressed q")
#     except:
#         print("no key")
#     currenttime = time.time()
#     print (f'the new time is {currenttime}' )
#     time.sleep(1)