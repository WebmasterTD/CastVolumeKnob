#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <Time.h>

#define WAKE_PIN 2
#define LED_V_PIN 4
#define INT_PIN 0
#define BUTTON 3

volatile int state = 30;

void setup() {
  GIMSK = 0b00100000;
  PCMSK = 0b00000001;
  ADCSRA &= ~_BV(ADEN);                   
  
  //Serial.begin(9600);
  pinMode(WAKE_PIN, OUTPUT);
  digitalWrite(WAKE_PIN, HIGH);
  pinMode(LED_V_PIN, INPUT);
  pinMode(BUTTON, OUTPUT);
  pinMode(INT_PIN, INPUT_PULLUP);
 
  sei();
  //attachInterrupt(digitalPinToInterrupt(INT_PIN), wake_up, LOW);
  }

void loop() {
  switch (state) {
    case 0:   //reset ESP 
      rst_esp();
      state = 10;
      break;
      
    case 5:   //TEST case
      delay(1000);
      state = 30;
      break;
      
    case 10:    //WAIT for ESP to turn on
      while (digitalRead(LED_V_PIN) == LOW) {
        delay(50);
      }
      state = 20;
      break;

    case 20:    //RUNNING --- WAIT for ESP to turn off     
      while (digitalRead(LED_V_PIN) == HIGH) {
        if (digitalRead(INT_PIN) == LOW){
          digitalWrite(BUTTON, HIGH);
          delay(100);
          digitalWrite(BUTTON, LOW);
        }
        delay(50);
        //Serial.println(state);
      }
      state = 30;
      break;
      
    case 30:
      //attachInterrupt(digitalPinToInterrupt(INT_PIN), wake_up, LOW);
      sei();
      state = 40;
      break;
    case 40:
      sleep();
  }
  delay(100);

}

/*
void wake_up() {
  detachInterrupt(digitalPinToInterrupt(INT_PIN));
  //sleep_disable();
  state = 0;
}
*/

ISR(PCINT0_vect)
{
  cli();
  state = 0;
}

void rst_esp() {
  digitalWrite(WAKE_PIN, LOW);
  delay(500);
  digitalWrite(WAKE_PIN, HIGH);
}

void sleep() {
    cli();
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);    // replaces above statement
    sleep_enable();                         // Sets the Sleep Enable bit in the MCUCR Register (SE BIT)
    sei();                                  // Enable interrupts
    sleep_cpu();                            // sleep
    } 
