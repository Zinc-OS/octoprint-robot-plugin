# Robot Control Plugin

Plugin for controling my robot

## Setup

Install manually using this URL:

    https://github.com/Zinc-OS/octoprint-robot-plugin/archive/master.zip



## Configuration

For a four servo robot. via the I2C bus

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
Servo myservoa,myservob,myservoc,myservod;
void setup() {
  Wire.begin(8);                // join i2c bus with address #3
  Wire.onReceive(receiveEvent); // register event
  myservoa.attach(9);  //the pin for the servoa control
  myservob.attach(10);  //the pin for the servob control
  myservoc.attach(11);  //the pin for the servoc control
  myservod.attach(12);  //the pin for the servod control
  myservoa.write(0);
  delay(100);
  myservoa.write(180);
  delay(100);
  myservoa.write(90);

  myservob.write(0);
  delay(100);
  myservob.write(180);
  delay(100);
  myservob.write(90);

  myservoc.write(0);
  delay(100);
  myservoc.write(180);
  delay(100);
  myservoc.write(90);

  myservod.write(0);
  delay(100);
  myservod.write(180);
  delay(100);
  myservod.write(90);
}

void loop() {
}
void receiveEvent(int howMany) {
  int c = Wire.read();
  if(c>32){
    if(c>64){
      if(c>96){
        myservoa.write((c-96)*6);
      }
      else{
        myservob.write((c-64)*6);
      }
    }
    else{
      myservoc.write((c-32)*6);
    }
  }
  else{
    myservod.write(c*6);
  }
}
```
Board setup:
![edit service](diagram.png)


