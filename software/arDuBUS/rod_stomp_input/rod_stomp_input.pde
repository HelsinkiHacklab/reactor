/**
 * Notes about ports on Seeduino Mega
 *
 * PORTA Pins 22-29
 * PORTB 53,52-50(SPI),10-13 (NOTE: pin13 has the led and it has resistor, thus the internal pull-up can't be used with it)
 * PORTC Pins 30-37
 * <PORTD 3-4(I2C),RX1-RX2,PD4-PD6,38>
 * <PORTE can't be used, had RX0/TX0 which we need.>
 * PORTF Analog normal 0-7
 * PORTG 39-41,4,PG4-PG3, (NOTE PG6-7 are missing)
 * PORTH RX2-TX2,PH2,6-9,PH7
 * PORTK Analog mega 8-15
 * PORTL Pins 42-49
 *
 * See timers http://softsolder.com/2010/09/05/arduino-mega-1280-pwm-to-timer-assignment/
 */
 
#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
// These don't seem to work: PE2, PE6, PE7, PG3, PG4, PD6, PD5, PD4, PJ7, PJ6, PJ5, PJ4, PJ3, PJ2, PH7, PH2 (the extra 16-pin header on seeeduino mega)
#define ARDUBUS_DIGITAL_INPUTS { 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53 } 
#include <ardubus.h>

void setup()
{
    Serial.begin(115200);
    // Set some I2C values that should not be set automagically by the library
    ardubus_setup();
    Serial.println("IM: rod_stomp_input");
    Serial.println("Booted");
}

void loop()
{
    ardubus_update();
}
