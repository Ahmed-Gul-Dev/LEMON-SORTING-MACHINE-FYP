#include <Servo.h>

const int startbtn = 2;
const int inching = 3;
const int servo = 9;
const int IRsensor = 5;
const int conveyor = 11;

int Yellow = 130;
int Green = 170;
int Rejected = 150;

Servo Sorter;  // create servo object to control a servo
bool enable = true;

void setup() {
  Serial.begin(9600);
  Sorter.attach(servo);
  Sorter.write(Rejected);

  pinMode(conveyor, OUTPUT);
  digitalWrite(conveyor, HIGH);

  pinMode(startbtn, INPUT_PULLUP);
  pinMode(inching, INPUT_PULLUP);
  pinMode(IRsensor, INPUT);
  Serial.println("System OK");
}

void loop() {
  if (digitalRead(startbtn) == LOW) {
    digitalWrite(conveyor, LOW);

    if (digitalRead(IRsensor) == LOW && enable) {
      delay(1200);
      Serial.println("Check");  // to Laptop Python Program
      delay(300);
      enable = false;
      digitalWrite(conveyor, HIGH);
    }
    while (enable == false) {
      if (Serial.available() > 0) {
        String data = Serial.readStringUntil('&');
        if (data == "Yellow") {
          Sorter.write(Yellow);
          delay(500);
          digitalWrite(conveyor, LOW);
          enable = true;
        } else if (data == "Green") {
          Sorter.write(Green);
          delay(500);
          digitalWrite(conveyor, LOW);
          enable = true;
        } else if (data == "Reject") {
          Sorter.write(Rejected);
          delay(500);
          digitalWrite(conveyor, LOW);
          enable = true;
        }
      }
    }

  } else {
    if (digitalRead(inching) == LOW) {
      digitalWrite(conveyor, LOW);
    } else {
      digitalWrite(conveyor, HIGH);
    }
  }
}
