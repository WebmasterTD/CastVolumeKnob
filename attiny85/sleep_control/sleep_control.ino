#include <avr/sleep.h>
#include <Time.h>

const byte ledPin = 13;
const byte interruptPin = 2;
volatile bool state = LOW;
volatile unsigned long timestamp = millis();
volatile bool interrupted = false;
void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
  
  Serial.println(timestamp);
  //set_sleep_mode(SLEEP_MODE_PWR_DOWN);
}

void loop() {
  digitalWrite(ledPin, state);
  /*if (interrupted)
  {
    Serial.println("interrupted");
    detachInterrupt(digitalPinToInterrupt(interruptPin));
  }*/
  if ((millis() - timestamp) > 1000)
  { 
    //Serial.println(millis() - timestamp);
    attachInterrupt(digitalPinToInterrupt(interruptPin), blink, FALLING);
  }
}

void blink() {
  detachInterrupt(digitalPinToInterrupt(interruptPin));
  //interrupted = true;
  state = !state;
  timestamp = millis();
}
