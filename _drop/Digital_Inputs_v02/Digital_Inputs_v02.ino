//www.elegoo.com
//2016.12.08

int ledPin = 5;
int buttonApin = 9;
int buttonBpin = 8;
unsigned long time;
unsigned long difference;


void setup() {
  Serial.begin(9600); // open the serial port at 9600 bps:
  pinMode(ledPin, OUTPUT);
  pinMode(buttonApin, INPUT_PULLUP);  
  pinMode(buttonBpin, INPUT_PULLUP);  
}
class Tool {
    public:
        char name;
        char status;
        int gate_prefs;
        char sensor_type[7] = "button";
        int sensor_pin;
        int amp_trigger;
        unsigned long last_used; //var is long because millis gets to be very big
        float spindown_time;
        void is_it_on() {
          if (sensor_type == "button"){
            Serial.println("tool button pressed");
          }
        }
int main(){
    Tool tablesaw;
    tablesaw.name = "TableSaw";
    tablesaw.status = "off";
    tablesaw.gate_prefs = {"closed","closed","closed","closed","closed","closed","open","open"};
    tablesaw.sensor_type = "button";
    tablesaw.sensor_pin = A1;
    tablesaw.amp_trigger = 10;
    tablesaw.last_used = 0;
    tablesaw.spindown_time = 45;
}

void loop() {
  //Serial.print("trying to print");
  //Serial.println();        // prints another carriage return
  if (digitalRead(buttonApin) == LOW){
    Serial.println("button A pressed");
    tablesaw.is_it_on();
    digitalWrite(ledPin, HIGH);
  }
  if (digitalRead(buttonBpin) == LOW){
    difference = millis()-time; 
    Serial.println("button B pressed");
    Serial.println(difference);
    digitalWrite(ledPin, LOW);
  }
// carriage return after the last label
}
