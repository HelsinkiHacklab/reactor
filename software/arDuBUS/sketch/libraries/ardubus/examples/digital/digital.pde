#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS { 2, 24, 32, 50, PJ6, 44 }
#define ARDUBUS_DIGITAL_OUTPUTS { 13 }
#define ARDUBUS_ANALOG_INPUTS { A1 }
#define ARDUBUS_PWM_OUTPUTS { 13 }
#include <Servo.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_SERVO_OUTPUTS { 10 }
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
