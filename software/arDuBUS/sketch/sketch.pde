#include <Wire.h>

/**
 * Notes about ports on Seeduino Mega
 *
 * PORTA Pins 22-29
 * PORTB 53,52-50(SPI),10-13
 * PORTC Pins 30-37
 * <PORTD 3-4(I2C),RX1-RX2,PD4-PD6,38>
 * <PORTE can't be used, had RX0/TX0 which we need.>
 * PORTF Analog normal 0-7
 * PORTG 39-41,4,PG4-PG3, (NOTE PG6-7 are missing)
 * PORTH RX2-TX2,PH2,6-9,PH7
 * PORTK Analog mega 8-15
 * PORTL Pins 42-49
 */


void setup()
{
    Serial.begin(115200);
    for (byte i=2; i<=13; i++)
    {
        pinMode(i, INPUT);
    }
    for (byte i=22; i<=29; i++)
    {
        pinMode(i, INPUT);
    }
    for (byte i=30; i<=37; i++)
    {
        pinMode(i, INPUT);
    }
    for (byte i=42; i<=49; i++)
    {
        pinMode(i, INPUT);
    }
    Serial.println('Analog pins');
    Serial.println(A0, DEC);
    Serial.println(A7, DEC);
    Serial.println(A8, DEC);
    Serial.println(A15, DEC);
    Serial.println("Booted");
}

byte pinstates[70];

void loop()
{
    unsigned long startms = millis();
    unsigned long startus = micros();
    byte foo;
    for (byte i=2; i<=13; i++)
    {
        pinstates[i] = digitalRead(i);
    }
    for (byte i=22; i<=29; i++)
    {
        pinstates[i] = digitalRead(i);
    }
    for (byte i=30; i<=37; i++)
    {
        pinstates[i] = digitalRead(i);
    }
    for (byte i=42; i<=49; i++)
    {
        pinstates[i] = digitalRead(i);
    }
    // Analog pins
    for (byte i=54; i<=69; i++)
    {
        pinstates[i] = digitalRead(i);
    }
    unsigned long endms = millis();
    unsigned long endus = micros();

    Serial.print("Reads took ");
    Serial.print(endms-startms, DEC);
    Serial.println("ms");
    Serial.print(startms, DEC);
    Serial.print(" ");
    Serial.println(endms, DEC);
    Serial.print("Reads took ");
    Serial.print(endus-startus, DEC);
    Serial.println("us");
    Serial.print(startus, DEC);
    Serial.print(" ");
    Serial.println(endus, DEC);
    Serial.println("Pin states:");
    for (byte i=2; i<=70; i++)
    {
        Serial.print(i, DEC);
        Serial.print("=");
        Serial.println(pinstates[i], DEC);
    }
    
    
    delay(100);
}
