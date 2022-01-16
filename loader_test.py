import os
from os.path import dirname, join
import get_full_path

backup_dir = '_BU'
dir_name = dirname(__file__)

full_path = join(dir_name, backup_dir)
path = ('/home/pi/Blinky/_BU')

files = os.listdir(path)
files.reverse()

print(files)