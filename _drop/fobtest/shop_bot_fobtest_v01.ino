//shopbot 
//setup
const int fobPin01 = 4;
const int fobPin02 = 5;
const int fobPin03 = 6;
const int fobPin04 = 7;
//const int dustCollectorRelayPin13 = 13;
int buttonState = 0;

void setup(){
	//initialize button pin as input
	pinMode(fobPin02, INPUT);
	//initialize relay pin as output
	//pinMode(dustCollectorRelayPin13, OUTPUT);


}


void loop() {
	//read the button state
	buttonState = digitalRead(fobPin02);

	if (buttonState == HIGH){
		//turn on relay
		Serial.print("key pressed");
	} else {
		//turn off relay
		Serial.print("key unpressed");
	}
}
