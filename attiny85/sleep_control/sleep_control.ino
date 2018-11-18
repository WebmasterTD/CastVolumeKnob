#include <avr/sleep.h>
#include <Time.h>

const byte ledPin = 13;
const byte interruptPin = 2;
volatile bool state = LOW;
volatile unsigned long timestamp = millis();
volatile bool interrupted = false;
bool prev_state = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT_PULLUP);
   //enable global interrupts
  Serial.println(millis());
  //set_sleep_mode(SLEEP_MODE_PWR_DOWN);
}

void loop() {
  digitalWrite(ledPin, state);
  /*if (interrupted)
  {
    Serial.println("interrupted");
    detachInterrupt(digitalPinToInterrupt(interruptPin));
  }*/
  if (state != prev_state)
  {
    prev_state = state;
    Serial.println(millis());
  }
  if ((millis() - timestamp) > 1000)
  { 
    attachInterrupt(digitalPinToInterrupt(interruptPin), wake_up, LOW);
    //set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    //cli(); //disable global interrupts
    //sleep_enable(); //enable sleep mode
    //sleep_bod_disable(); //Brown out detection
    //sei();
    //sleep_cpu(); //activating sleep mode
  }
}

void wake_up() {
  detachInterrupt(digitalPinToInterrupt(interruptPin));
  //sleep_disable();
  //interrupted = true;
  //Serial.println(millis());
  state = !state;
  timestamp = millis();
}
