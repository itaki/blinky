/* This code works with ACS712 current sensor, it permits to calculate the RMS of a sinewave Alternating Current
 * it uses the Peak to Peak method to calculate the RMS
 * For more information check www.surtrtech.com
 */

#define SAMPLES 300   //Number of samples you want to take everytime you loop
#define ACS_pin A0    //ACS712 data pin analong input
#define dusty 13     //Dust collection relay 1 (Note: since the collector is 220 it uses 2 relays - could map them together)
#define sensitivity 8 //generally when it's off it's around 5-6

float High_peak,Low_peak;         //Variables to measure or calculate
float Amps_Peak_Peak, Amps_RMS;
uint8_t sensors[] = {A0, A1, A2};
uint8_t number_of_tools = sizeof(sensors) / sizeof(uint8_t);
boolean collectorIsOn = 0;
int pin;

void setup() 
{
  Serial.begin(9600);
  pinMode(ACS_pin,INPUT);        //Define pin mode
  pinMode(dusty, OUTPUT);      //Define dusty relay
  digitalWrite(dusty, LOW);
}
//define variables
void loop() 
{
  for(int i=0;i<number_of_tools;i++){
    pin = sensors[i];
    tool_status(pin);                               //Launch the read_Amps function
    Amps_RMS = Amps_Peak_Peak*0.3536*0.06;     //Now we have the peak to peak value normally the formula requires only multiplying times 0.3536
                                             //but since the values will be very big you should multiply by 0.06, you can first not use it, 
                                             //do your calculations and compare them to real values measured by an Ammeter. eg: 0.06=Real value/Measured value
                                             
    Serial.print(pin);
    Serial.print("\t");
    Serial.print(Amps_RMS);                    //Here I show the RMS value and the peak to peak value, you can print what you want and add the "A" symbol...
    Serial.print("\t");
    Serial.println(Amps_Peak_Peak);
    if (Amps_Peak_Peak>10){
      digitalWrite(dusty, HIGH);

  } else {
    digitalWrite(dusty, LOW);
  }
  delay(200);

  }

}

float tool_status(int tool_number)            //read_Amps function calculate the difference between the high peak and low peak 
{                           //get peak to peak value
  int cnt;            //Counter
  High_peak = 0;      //We first assume that our high peak is equal to 0 and low peak is 1024, yes inverted
  Low_peak = 1024;
  
      for(cnt=0 ; cnt<SAMPLES ; cnt++)          //everytime a sample (module value) is taken it will go through test
      {
        float ACS_Value = analogRead(pin); //We read a single value from the module

        
        if(ACS_Value > High_peak)                //If that value is higher than the high peak (at first is 0)
            {
              High_peak = ACS_Value;            //The high peak will change from 0 to that value found
            }
        
        if(ACS_Value < Low_peak)                //If that value is lower than the low peak (at first is 1024)
            {
              Low_peak = ACS_Value;             //The low peak will change from 1024 to that value found
            }
      }                                        //We keep looping until we take all samples and at the end we will have the high/low peaks values
      
  Amps_Peak_Peak = High_peak - Low_peak;      //Calculate the difference
}
