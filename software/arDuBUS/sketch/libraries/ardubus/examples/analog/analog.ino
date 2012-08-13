/**
 * Setup a potentiometer with wiper (middle) connected to analog 0 and the other leads to GND and +5V
 * Load this sketch to an arduino and run the ardubus.py and ardubus_listener.py on the host machine.
 */
#define ARDUBUS_ANALOG_INPUTS { A0 }
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
