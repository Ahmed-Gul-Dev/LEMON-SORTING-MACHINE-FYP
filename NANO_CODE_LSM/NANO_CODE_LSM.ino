/*
Arduino Nano
Muhammad Taha
0330-8530186
*/

#include <Servo.h>
const int StartPin =2;  // Holding Switch INPUT
const int StopPin = 2;   // Holding Switch INPUT
const int Inching = 3;

const int IRSensorPin = 5;  // IR Sensor INPUT
const int SensorSpare = 6;  // IR Sensor INPUT

const int ConveyourPin = 11;  // Conveyour Relay
const int Relay2 = 12;        // Conveyour Relay
const int ServoPin = 9;       // Servo Motor Pin

int Yellow = 130;
int Green = 170;
int Rejected = 150;

Servo Sorter;  // create servo object to control a servo
int tick = 0;

bool ON = LOW;
bool OFF = HIGH;

void setup() {
  Serial.begin(9600);
  Sorter.attach(ServoPin);
  Sorter.write(Rejected);

  pinMode(StartPin, INPUT_PULLUP);
  pinMode(StopPin, INPUT_PULLUP);
  pinMode(Inching, INPUT_PULLUP);
  pinMode(IRSensorPin, INPUT);

  pinMode(ConveyourPin, OUTPUT);
  digitalWrite(ConveyourPin, OFF);
  Serial.println("System OK");
}

void loop() {

  if (digitalRead(StartPin) == LOW) {
    digitalWrite(ConveyourPin, ON);

    while (digitalRead(StartPin) == LOW) {

      if (digitalRead(IRSensorPin) == LOW && tick == 0) {
        digitalWrite(ConveyourPin, OFF);
        delay(100);
        Serial.println("Check");
        tick = 1;
        delay(250);
      } else {
        if (Serial.available() > 0) {
          String Data = Serial.readStringUntil('&');
          if (Data == "Green") {
            Sorter.write(Green);
            digitalWrite(ConveyourPin, ON);
            delay(500);
            tick = 0;
          } else if (Data == "Yellow") {
            Sorter.write(Yellow);
            digitalWrite(ConveyourPin, ON);
            delay(500);
            tick = 0;
          } else if (Data == "Reject") {
            Sorter.write(Rejected);
            digitalWrite(ConveyourPin, ON);
            delay(500);
            tick = 0;
          } else {
            Serial.println("Error");
            tick = 0;
          }
        }
      }
    }
  }

  else {
    if (digitalRead(Inching) == LOW) {
      digitalWrite(ConveyourPin, ON);
    } else {
      digitalWrite(ConveyourPin, OFF);
    }
  }
}
