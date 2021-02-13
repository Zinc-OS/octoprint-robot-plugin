#include <Wire.h>
#include <Servo.h>
const int ledPin = 13; // onboard LED
static_assert(LOW == 0, "Expecting LOW to be 0");
const int servos=4;//The number of servos used
Servo servo[servos];
//current servo do not change
int current_servo=0;
//servo pins--change these to the pins you want to use
const byte servoPins[] = {12,11,10,9,8,7,6,5,4,3,2};
//
void setup() {
  Wire.begin(8);                // join i2c bus with address #3
  Wire.onReceive(receiveEvent); // register event
  
}

void loop() {
}
void receiveEvent(int howMany) {
  int c = Wire.read();
  if(c>=0b10000000){
    current_servo=c-128;
  }else{
    if(servo[current_servo].attached()){
      servo[current_servo].write(c*2);
    }else if(current_servo<=servos){
      servo[current_servo].attach(servoPins[current_servo]);
      servo[current_servo].write(c*2);
    }
      
        
    }
  
}
