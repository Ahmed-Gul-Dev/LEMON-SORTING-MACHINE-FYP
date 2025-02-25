#include <LiquidCrystal.h>  // includes the LiquidCrystal Library
#include <Servo.h>

#define factor 10.0 // to be changed for increasing Time Delay

LiquidCrystal lcd(2, 3, 4, 5, 6, 7);
Servo Barrier;  // create servo object to control a servo

const int motor = A0;

void setup() {
  Serial.begin(9600);

  pinMode(A2, INPUT);
  Barrier.attach(9);
  Barrier.write(0);

  pinMode(motor, OUTPUT);
  digitalWrite(motor, HIGH);

  lcd.begin(16, 2);
  lcd.clear();
  delay(1000);
}

double Raw = 0;

void loop() {
  Raw = (double)analogRead(A2);
  Raw =  (Raw * factor) / 1000;

  lcd.setCursor(0, 0);
  lcd.print("Time: ");
  lcd.setCursor(8, 0);
  lcd.print(Raw);
  lcd.print(" s");

  digitalWrite(motor, LOW);
  delay(500);
  digitalWrite(motor, HIGH);

  Barrier.write(60);
  delay(300);
  Barrier.write(0);
  Raw = Raw * 1000;
  delay(Raw);
}