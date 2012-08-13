/**
 * Connect a servo with the signal wire (with) to pin 10 on the arduino, GND (black) to arduino GND and +5V to external power
 * (or if it's a *very* small servo to +5V on arduino), if using external power connect arduino GND to external GND too
 * On host computer run ardubus.py and ardubus_consumer.py (and use the consumer to call the DBUS servo methods)
 */
#include <Servo.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_SERVO_OUTPUTS { 10 }
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
