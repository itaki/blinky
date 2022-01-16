//shopbot 
//setup
const int fobPin02 = 2;
const int dustCollectorRelayPin12 = 12;
const int dustCollectorRelayPin13 = 13;

int buttonState = 0;

void setup(){
	//initialize button pin as input
	pinMode(fobPin02, INPUT);
	//initialize relay pin as output
	pinMode(dustCollectorRelayPin13, OUTPUT);


}


void loop() {
	//read the button state
	buttonState = digitalRead(fobPin02);

	if (buttonState == HIGH){
		//turn on relay
		digitalWrite(dustCollectorRelayPin12, HIGH);
		digitalWrite(dustCollectorRelayPin13, HIGH);
	} else {
		//turn off relay
		digitalWrite(dustCollectorRelayPin12, LOW);
		digitalWrite(dustCollectorRelayPin13, LOW);
	}
}




//read pin 