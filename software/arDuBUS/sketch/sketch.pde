#include <Bounce.h>

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
 

Bounce bouncers[70] = Bounce(2, 20); // We must initialize these or things break

void setup()
{
    Serial.begin(115200);
    for (byte i=2; i<=13; i++)
    {
        pinMode(i, INPUT);
        digitalWrite(i, HIGH); // enable internal pull-up
        bouncers[i] = Bounce(i, 20);
    }
    for (byte i=22; i<=29; i++)
    {
        pinMode(i, INPUT);
        digitalWrite(i, HIGH); // enable internal pull-up
        bouncers[i] = Bounce(i, 20);
    }
    for (byte i=30; i<=37; i++)
    {
        pinMode(i, INPUT);
        digitalWrite(i, HIGH); // enable internal pull-up
        bouncers[i] = Bounce(i, 20);
    }
    for (byte i=42; i<=49; i++)
    {
        pinMode(i, INPUT);
        digitalWrite(i, HIGH); // enable internal pull-up
        bouncers[i] = Bounce(i, 20);
    }
    /*
    // Analog inputs are already inputs
    for (byte i=54; i<=69; i++)
    {
        pinMode(i, INPUT);
        digitalWrite(i, HIGH); // enable internal pull-up
        bouncers[i] = Bounce(i, 20);
    }
    */
    Serial.println("Booted");
}

byte pinstates[70];

unsigned int iter;
void loop()
{
    iter++;
    Serial.print("Iteration #");
    Serial.println(iter, DEC);
    unsigned long startms = millis();
    unsigned long startus = micros();
    // Update states
    for (byte i=2; i<=13; i++)
    {
        bouncers[i].update();
        pinstates[i] = bouncers[i].read();
    }
    for (byte i=22; i<=29; i++)
    {
        bouncers[i].update();
        pinstates[i] = bouncers[i].read();
    }
    for (byte i=30; i<=37; i++)
    {
        bouncers[i].update();
        pinstates[i] = bouncers[i].read();
    }
    for (byte i=42; i<=49; i++)
    {
        bouncers[i].update();
        pinstates[i] = bouncers[i].read();
    }
    /*
    // Analog inputs are already inputs
    for (byte i=54; i<=69; i++)
    {
        bouncers[i].update();
        pinstates[i] = bouncers[i].read();
    }
    */
    unsigned long endms = millis();
    unsigned long endus = micros();

    Serial.print("updates&reads took ");
    Serial.print(endms-startms, DEC);
    Serial.println("ms");
    Serial.print(startms, DEC);
    Serial.print(" ");
    Serial.println(endms, DEC);
    Serial.print("updates took ");
    Serial.print(endus-startus, DEC);
    Serial.println("us");
    Serial.print(startus, DEC);
    Serial.print(" ");
    Serial.println(endus, DEC);

    Serial.println("Pin states:");
    for (byte i=2; i<=49; i++)
    {
        Serial.print(i, DEC);
        Serial.print("=");
        Serial.println(pinstates[i], DEC);
    }

    delay(1000);
}
