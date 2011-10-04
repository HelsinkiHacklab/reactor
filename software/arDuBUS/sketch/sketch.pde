#include <Bounce.h>
#include <MsTimer2.h>

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

boolean update_bouncers_flag;
void flag_update_bouncer()
{
    update_bouncers_flag = true;
}

inline void setup_bouncer()
{
    // Setup the debouncers
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        pinMode(inputpins[i], INPUT);
        digitalWrite(inputpins[i], HIGH); // enable internal pull-up
        bouncers[i] = Bounce(inputpins[i], DEBOUNCE_TIME);
    }
}

inline void update_bouncers()
{
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
    update_bouncers_flag = false;
}

void setup()
{
    Serial.begin(115200);
    
    setup_bouncer();
    // Setup timer for flagging bouncer updates
    MsTimer2::set(5, flag_update_bouncer);
    MsTimer2::start();

    Serial.println("Booted");
}

void loop()
{
    if (update_bouncers_flag)
    {
        update_bouncers();
    }
}
