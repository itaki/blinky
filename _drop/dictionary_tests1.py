#keyboard version of blinky
import curses
import time
import json
from os.path import dirname, join

tool_ids = []
tool_names = []

def init(): #
    current_dir = dirname(__file__)                         #get current working directory
    file_path = join(current_dir, "./tools_list.json")      #set the file path
    with open(file_path, 'r') as tools_list:                #read the tool list
        tools = json.load(tools_list)   


init()
