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
        delay(100);
      }
      else{
        myservob.write((c-64)*6);
        delay(100);
      }
    }
    else{
      myservoc.write((c-32)*6);
      delay(100);
    }
  }
  else{
    myservod.write(c*6);
    delay(100);
  }
}
