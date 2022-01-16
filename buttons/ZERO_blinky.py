from gpiozero import LED, Button
from signal import pause
from time import sleep
led18 = LED(25)
button23 = Button(17)
previous_state = 1
current_state = 0

class Tool:
    def __init__(self, 
    name: str, 
    status: str='off', 
    gate_prefs=[0,0,0,0,0,1,1,0], 
    sensor_type: str='button', 
    sensor_pin=23, 
    amp_trigger=0, 
    last_used=0, 
    spin_down_time=45 ):
        self.name = name
        self.status = status
        self.gate_prefs = gate_prefs
        self.sensor_type = sensor_type
        self.sensor_pin = sensor_pin
        self.amp_trigger = amp_trigger
        self.last_used = last_used
        self.spin_down_time = spin_down_time



tablesaw = Tool('Tablesaw')

while True:
   if button23.when_pressed:
      if tablesaw.status != current_state:
         led18.on()
         current_state = 1
         print("tablesaw is on")
         sleep(0.15)

      else:
         led18.off()
         current_state = 0
         print("tablesaw is off")
         sleep(0.15)