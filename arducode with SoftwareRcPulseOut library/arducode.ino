#include <Wire.h>
#include <SoftRcPulseOut.h> 
const int ledPin = 13; // onboard LED
static_assert(LOW == 0, "Expecting LOW to be 0");
const int servos=4;//The number of servos used
SoftRcPulseOut servo[servos-1];
//current servo do not change
int current_servo=0;
//servo pins--change these to the pins you want to use
const int servoPins[] = {12,11,10,9};
//
void setup() {
  Serial.begin(9600);
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  for(int i=0; i<servos; i++){
    servo[i].attach(servoPins[i]);
    Serial.println(i);
  }
}

void loop() {

}
void receiveEvent(int howMany) {
  int c = Wire.read();
  Serial.println(c); 
  if(c>=128){
    current_servo=c-128;
  }else if(current_servo<servos){
      servo[current_servo].write(c*2);
      delay(5);
      SoftRcPulseOut::refresh(1); 
      
  }
  
    
  
}
