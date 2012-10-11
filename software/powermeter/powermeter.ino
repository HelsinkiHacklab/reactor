#include <LiquidCrystalFast.h>

/*
LiquidCrystalFast lcd(RS, RW, Enable, D4, D5, D6, D7) 
*/

#define VCC_MV (5200) // I'm using 5.2V supply
#define MV_PER_LSB ((uint8_t)(VCC_MV/1024)) // I sure hope the complier will optimize this result to a constant
#define ACS715_ZERO ((uint16_t)(VCC_MV/10))
#define ACS714_ZERO ((uint16_t)(VCC_MV/2))


LiquidCrystalFast lcd(0, 1, 2, 7, 8, 9, 10);

uint16_t acs715_mv2ma(uint16_t mv)
{
    // 133 mV/A starting at 500 mV (actually vcc/100), 1.5% error
    if (mv <= ACS715_ZERO)
    {
        return 0;
    }
    mv = mv - ACS715_ZERO; // Zero
    uint8_t amps = mv / 133;
    uint8_t desiamps = (mv - (amps*133)) / 13;
    uint8_t centiamps = (mv - (amps*133) - (desiamps*13));
    return (amps*1000) + (desiamps * 100) + (centiamps * 10);
}

inline int8_t acs714_mv2ma_sign(uint16_t mv)
{
    if (mv < ACS714_ZERO)
    {
        return -1;
    }
    return 1;
}

uint16_t acs714_mv2ma(uint16_t mv)
{
    // TODO: check if the 2500mv center point applies on 5.2V supply
    // 66mV/A centered on 2500mv, 1.5% error
    
    // For now I'll just care about the positive side.
    if (mv <= ACS714_ZERO)
    {
        return 0;
    }
    mv = mv - ACS714_ZERO;
    uint8_t amps = mv / 66;
    uint8_t desiamps = (mv - (amps*66)) / 6;
    return (amps*1000) + (desiamps * 100);
}

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
