#include < avr/io.h >
#include < avr/interrupt.h >


// LED connected to digital pin 13
int ledPin = 13;
// This is the INT0 Pin of the ATMega8
int sensePin = 2;
// We need to declare the data exchange
// variable to be volatile - the value is
// read from memory.
volatile int value = 0;

// Install the interrupt routine.
ISR(INT0_vect) {
  // check the value again - since it takes some time to
  // activate the interrupt routine, we get a clear signal.
  value = digitalRead(sensePin);
}


void setup() {
  Serial.begin(9600);
  Serial.println("Initializing ihandler");
  // sets the digital pin as output
  pinMode(ledPin, OUTPUT);
  // read from the sense pin
  pinMode(sensePin, INPUT);
  Serial.println("Processing initialization");
  // Global Enable INT0 interrupt
  GICR |= ( 1 < < INT0);
  // Signal change triggers interrupt
  MCUCR |= ( 1 << ISC00);
  MCUCR |= ( 0 << ISC01);
  Serial.println("Finished initialization");
}

void loop() {
  if (value) {
    Serial.println("Value high!");
    digitalWrite(ledPin, HIGH);
  } else {
    Serial.println("Value low!");
    digitalWrite(ledPin, LOW);
  }
  delay(100);
}