#blinky the shop bot
#https://www.youtube.com/watch?v=6qFp5vjkYk0&t=1s&ab_channel=MUO
import time


class Tool:
    def __init__(self, name, status, gate_prefs, sensor_type, sensor_pin, amp_trigger, last_used, spin_down_time ):
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



class Sensor:
    def __init__(self, sensor_name, sensor_type, sensor_pin,):
        self.name = sensor_name
        self.type = sensor_type
        self.pin = sensor_pin

    def 



int: is_it_on()
{
if sensor_type == "button"){
if (button_pressed == true)
{
if status == "on"
{
    status = "spindown";
last_used = millis;
}
else {
    tool['status'] == "on";
}

}
}
}
else if (tool['sensor_type'] == "voltage"){
amps = voltage_sensor.get_amps(tool["pin_number"]);
if (amps < tool["amp_trigger"]){
if tool["status"] == "on";
tool["status"] == "spindown";
tool['lastused'] == time.getTime();

}
if (amps > tool["amp_trigger"]){
tool['status'] == "on";
}
}
if (tool['status'] == "on"){
gatekeeper.set_gates(tool.gate_prefs);
dusty.spinup();
}
if (tool['status'] == "spindown"){
if time.getTime() - tool["lastused"] > tool["spindown_time"]{
tool['status'] == "off";
}

}
if (tool['status'] == "off"){
gatekeeper.set_gates(tool.gate_prefs);
dusty.spindown();
}
}
}

}

int
main()
{
    tool
tablesaw;
tablesaw.name = "TableSaw";
tablesaw.status = "off";
tablesaw.gate_prefs = {"closed", "closed", "closed", "closed", "closed", "closed", "open", "open"};
tablesaw.sensor_type = "voltage";
tablesaw.sensor_pin = A1;
tablesaw.amp_trigger = 10;
tablesaw.last_used = 0;
tablesaw.spindown_time = 45;
}

void
setup()
{
// initialize
button
pin as input
pinMode(fobPin02, INPUT);
// initialize
relay
pin as output
pinMode(dustCollectorRelayPin13, OUTPUT);

}

// main
loop
void
loop()
{
// loop
trhough
tools and set
status
for (int i=0;i < number_of_tools;i++) {
                                      // determine what type of sensor is being used
toollist.tool.am_i_on();

// end main loop
void tool.am_i_on(){

void
gatekeeper.set_gates(array
gate_prefs){
if (shopmanager.any_tool_on() == true)
{
for (int i=0;i < number_of_gates, i++) {
if (gate_prefs[i] == "open"){
gatekeeper.gate_status[i] == "open";

}
}
} else {
gatekeeper.gate_status == gate_prefs
}
// set the gates
for (int i=0;i < nubmer_of_gates;i++){
if (gatelist[i][status] == "open"){
gatekeeper.open_gate(i);
} else {
gatekeeper.close_gate(i);
}
}

void gatekeeper.close_gate(uint8_t num){
Serial.print("closeGate ");
Serial.println(num);
pwm.setPWM(num, 0, gatekeeper[num][min][1]);
}
void gatekeeper.open_gate(uint8_t num){
Serial.print("openGate ");
Serial.println(num);
pwm.setPWM(num, 0, gatekeeper[num][max][0]);
delay(100);
pwm.setPWM(num, 0, gatekeeper[num][max][0]-5);

shopmanager.any_tool_on(tools){
for (int i=0;i < number_of_tools;i++){
if (tools[i]['on'] == true){
return (true);
}
} else {
return (false);
}
}



dusty.spinup()
{
if (dusty == off)
{ // if dust
collector is off
digitalWrite(dusty_pin, HIGH); // turn
it
on(don
't think I need the if)
}
}
dusty.spindown()
{
if (shopmanager.any_tool_on() == false){// check to see if other tools are on
digitalWrite(dusty_pin, LOW); // if the aren't turn off the dust collector
}
}