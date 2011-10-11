#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS {}
#define ARDUBUS_DIGITAL_OUTPUTS {}
#define ARDUBUS_ANALOG_INPUTS {}
#define ARDUBUS_PWM_OUTPUTS {}
#include <Servo.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_SERVO_OUTPUTS {}
#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    ardubus_setup();
    Serial.println("Booted");
}

void loop()
{
    ardubus_update();
}
