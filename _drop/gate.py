from adafruit_servokit import ServoKit
import get_full_path
import os
import json
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
servo_hat = ServoKit(channels=16, address  = 0x40)


class Gate:
    def __init__(self, name, gate_id, location, status, address, minimum, maximum, info):
        self.name = name
        self.gate_id = gate_id
        self.location = location
        self.status = status
        self.address = address
        self.min = minimum
        self.max = maximum
        
        kit = ServoKit(channels=16)

    def open(self):

        kit.servo[self.pin].angle = self.max
        print(f'opening {self.name}')
        # send maximum to gate
        self.status = 0

       

    def close(self):

        kit.servo[self.pin].angle = self.min
        print(f'closing {self.name}')
        # send minimum to gate
        self.status = 1


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
                gate['gate_id'],
                gate['location'],
                gate['status'],
                gate['address'],
                gate['min'],
                gate['max'],
                gate['info']
            )
            # 1print(tool)
    return(gates)
    #print(f'These are your tools {gates}')

### Main application
if __name__ == "__main__":
    tools = blinky_bits.get_tools()
    tools_with_v_sensor = get_tools_with_sensor(tools)
    while True:
        show_all_tools_status(tools_with_v_sensor)
        time.sleep(.5)