#include <Servo.h>
Servo myservo;  // create servo object to control a servo
void setup() { myservo.attach(9); } // attaches the servo on pin 9 to the servo object
void loop() {
  int val1;
  int val3;
  val1 = analogRead(0);
  val3 = analogRead(2);
  int threshold = 500;
  if(val1 < threshold | val3 < threshold){
    myservo.write(90);
    delay(2000);
  } else { myservo.write(0); }
}