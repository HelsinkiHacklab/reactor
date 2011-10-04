#include <Bounce.h>

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

// Define the input pins we wish to use
const byte inputpins[] = { 2, 24, 32, 50, PJ6, 44 };
#define DEBOUNCE_TIME 20 // milliseconds, see Bounce library

// Initialize the array of debouncers
Bounce bouncers[sizeof(inputpins)] = Bounce(inputpins[0],DEBOUNCE_TIME); // We must initialize these or things break

void setup()
{
    Serial.begin(115200);
    
    // Setup the debouncers
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        pinMode(inputpins[i], INPUT);
        digitalWrite(inputpins[i], HIGH); // enable internal pull-up
        bouncers[i] = Bounce(inputpins[i], DEBOUNCE_TIME);
    }

    Serial.println("Booted");
}

unsigned int iter;
void loop()
{
    iter++;
    Serial.print("Iteration #");
    Serial.println(iter, DEC);
    unsigned long startms = millis();
    unsigned long startus = micros();

    // Update debouncer states
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        if (bouncers[i].update())
        {
            // State changed
            Serial.print("Pin ");
            Serial.print(inputpins[i], DEC);
            Serial.print(" CHANGED to ");
            Serial.println(bouncers[i].read(), DEC);
        }
    }

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
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        Serial.print("Pin ");
        Serial.print(inputpins[i], DEC);
        Serial.print(" state is ");
        Serial.println(bouncers[i].read(), DEC);
    }

    delay(1000);
}
