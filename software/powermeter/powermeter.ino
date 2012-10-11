#include <LiquidCrystalFast.h>

/*
LiquidCrystalFast lcd(RS, RW, Enable, D4, D5, D6, D7) 
*/

LiquidCrystalFast lcd(0, 1, 2, 7, 8, 9, 10);

uint16_t pa4;
uint16_t pa5;
uint16_t pa6;
uint16_t pa7;

char lcdline1[17];
char lcdline2[17];

void setup() {
  // set up the LCD's number of rows and columns: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("hello, world!");
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  delay(500);
  lcd.clear();
}

void loop() {
  pa4 = analogRead(A4);
  pa5 = analogRead(A5);
  pa6 = analogRead(A6);
  pa7 = analogRead(A7);

  sprintf(lcdline1, "%04d | %04d", pa4, pa5);
  lcd.setCursor(0, 0);
  lcd.print(lcdline1);
  sprintf(lcdline2, "%04d | %04d", pa6, pa7);
  lcd.setCursor(0, 1);
  lcd.print(lcdline2);

  /*
  lcd.clear();
  lcd.print(pa4, DEC);
  lcd.print("|");
  lcd.print(pa5, DEC);

  lcd.setCursor(0, 1);
  lcd.print(pa5, DEC);
  lcd.print("|");
  lcd.print(pa6, DEC);
  */
  delay(500);
}
