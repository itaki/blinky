#keyboard version of blinky
import time
import json

# Opening JSON file
f = open('tools.json')
 
# returns JSON object as
# a dictionary
tools = json.load(f)
 
# Iterating through the json
# list
for i in tools:
    print(i)
 
# Closing file
f.close()

class Tool:
    def __init__(self, id_num, name, status, gate_prefs, sensor_type, sensor_pin, amp_trigger, last_used, spin_down_time ):
        self.id_num = id_num
        self.name = name
        self.status = status
        self.gate_prefs = gate_prefs
        self.sensor_type = sensor_type
        self.sensor_pin = sensor_pin
        self.amp_trigger = amp_trigger
        self.last_used = last_used
        self.spin_down_time = spin_down_time
    def am_i_on(self):
        if (self.sensor_type == 'button'):
            if (self.button_pressed == True):
                if (self.status == 'on'):
                    status = 'spindown'
                    last_used = time.getTime()
                else:
                    status ='on'
        elif (self.sensor_type == 'voltage'):
            amps = self.voltage_sensor.get_amps(self.pin_number)
            if (amps < self.amp_trigger):
                if (self.status == 'on'):
                    status = 'spindown'
                    last_used = time.getTime()
            elif (amps > self.amp_trigger):
                self.status 



while True:
    tool = int(input ("select tool"))
    if (tool == 1):
        print ("tool 1 selected")
        status = tool
    else:
        print ("not tool1")
