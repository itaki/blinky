import keypress_module as kp
from os.path import dirname, join
import json


def init():
    kp.init() # start the keypress module
    current_dir = dirname(__file__)
    file_path = join(current_dir, "./tools.json")
    with open(file_path, 'r') as tools_list:
	    tools = json.load(tools_list)
    dump = json.dumps(tools, indent=4)
    print(dump)


def main():
    keypressed = kp.get_key('1')
    print( keypressed )

   


if __name__ == '__main__':
    init()
    while True:
        main()