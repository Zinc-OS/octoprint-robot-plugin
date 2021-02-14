# Robot Control Plugin

Plugin for controling my robot  via the I2C bus.

## Setup

Install manually using this URL:

    https://github.com/Zinc-OS/octoprint-robot-plugin/archive/master.zip



## Configuration

For a servo-controlled robot. You can use as many servos as your board can hold(with a limit of 127)

You will also need to enable i2c bus via ```sudo raspi-cofig``` through the terminal, accessible through ```ssh pi@octopi.local:22```

then
```interface options>enable i2c>yes>finish```

For the raspi, addresses cannot be lower than 3, and the arduino only use addresses higher than 8, so the address must be an integer 8-127, and must be the same for the adruino and the raspi.

There are sliders in the robot control tab, and gcodes can be used with the format ```@servo[1..4]:[ANGLE]```, such as ```@servo2:90``` or ```@servo4:12```.


Arduino code:
```
#include <Wire.h>
#include <Servo.h>
const int ledPin = 13; // onboard LED
static_assert(LOW == 0, "Expecting LOW to be 0");
const int servos=4;//The number of servos used
Servo servo[servos-1];
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
      
  }
  
    
  
}
```
Board setup:
![edit service](diagram.png)


