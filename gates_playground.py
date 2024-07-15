import board
import busio
import get_full_path
import os
import json
import random

from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit

i2c_bus = busio.I2C(board.SCL, board.SDA)

gates_file = "gates.json"

class Gate:
    def __init__(self, name, gate_id, physical_location, status, io_location, minimum, maximum, info):
        self.name = name
        self.id = gate_id
        self.physical_location = physical_location
        self.status = status
        self.io_location = io_location
        self.min = minimum
        self.max = maximum
        self.info = info



def get_gates(file): 
    gates_list = []  # list
    gates = {}
        # LOAD ALL THE GATES
    if os.path.exists(file): # if there is a gates file load it
        file_path = get_full_path.path(file)  # set the file path
        with open(file_path, 'r') as f:  # read the gate list
            gates_list = json.load(f)  # load gate list into python

        for gate in gates_list:
            gates[gate['name']] = Gate(
                gate['name'],
                gate['id'],
                gate['physical_location'],
                gate['status'],
                gate['io_location'],
                gate['min'],
                gate['max'],
                gate['info']
            )
            # 1print(tool)
    return(gates)
    #print(f'These are your tools {gates}')

def get_gate_board_addresses(gates):
    for gate in gates:
        selected_gate = gates[gate]
        print(selected_gate.io_location['address'])




def __main__():
    while True:
        pass


if __name__ == "__main__":
    rand_gate_degree = random.randrange(0, 180)
    gates = get_gates(gates_file)
    for gate in gates:
        print(f"{gate}")
    get_gate_board_addresses(gates)
    selected_gate = gates['MR']
    hex_address = hex(selected_gate.io_location['address'])
    print(f"location {selected_gate.io_location['address']} hex address {hex_address} pin {selected_gate.io_location['pin']}")
    selected_gate.location = ServoKit(channels=16, address = selected_gate.io_location['address']).servo[selected_gate.io_location['pin']]
    selected_gate.location.angle = rand_gate_degree
    # print (selected_gate.location)
    # selected_gate.location.angle = rand_gate_degree
    # ServoKit(channels=16, address=0x43).servo[0].angle = random.randrange(0, 180)