#gate questionary
import questionary as q
import shutil #allows for copying a file to make a backup
import os
from styles import custom_style_dope
import blinky_bits
import time
from datetime import datetime
import json
import errno
#style the questions
style = custom_style_dope


gates_file = 'gates.json'
backup_directory = '_BU'
force_backup = True

def create_directory(dir):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def backup_file(backup_directory, file):
    name_parts = file.split ('.')
    f_name = name_parts[0]
    ext = name_parts[-1]
    now = datetime.now() # get the current time
    tail = now.strftime('%Y%m%d-%H%M%S')
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    destination = backup_directory+'/'+f_name+'_'+tail+'.'+ext
    shutil.copy (file, destination)
    print(f"{file} backed up to {destination}")


def backup_needed(file):
    if os.path.exists(file): #there is already a gates file, should I load it?
        if force_backup: #automatically backup file at beginning of modification
            backup_file(file)
    else:
        my_choices = ['YES',
        'NO']
        action = q.select(f"You don't have auto backup ups on and are about to overwrite your {file} file.\n Would you like to backup this file now?", choices = my_choices, style = style).ask()
        if action == 'YES':
            backup_file(file)

def main_menu():
    choices = (
        'manage gates',
        'manage tools',
        'manage dust collectors'
    )

if __name__ == '__main__':
    print ("Welcome to the ITAKI shop manager")
    ### main menu

