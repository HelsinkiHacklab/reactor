/**
 * Connect switched to arduino pins 2 & 3 so that they close to ground (the library uses the internal pull-ups)
 * On host computer run ardubus.py and ardubus_listener.py and flip the switches.
 * To test outputs run ardubus_consumer.py and call the relevant methods
 */
#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS { 2, 3 }
#define ARDUBUS_DIGITAL_OUTPUTS { 13 }
#define ARDUBUS_PWM_OUTPUTS { 13 }
#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    ardubus_setup();
    Serial.println(F("Booted"));
}

void loop()
{
    ardubus_update();
}
