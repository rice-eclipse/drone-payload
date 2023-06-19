#include <Servo.h>
Servo myservo;  // create servo object to control a servo

unsigned int previous_time = millis(); //get the time at the beginning of the intialization
bool led_state = false; //feedback LED state tracker
int interval = 500; //set the time interval in milliseconds for flipping the feedback LED

void setup() { 
  pinMode(13, OUTPUT); //initialize feedback LED
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  //feedback code
  unsigned int current_time = millis();
  if(current_time >= previous_time + 500) {
    led_state = !led_state; //flip the led state
    digitalWrite(13, (led_state) ? HIGH : LOW);
    previous_time = current_time;
  }

  //actual code that actually runs
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