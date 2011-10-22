#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, A0, A1, A2, A3, A4, A5 }
#include <Servo.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_SERVO_OUTPUTS { 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53 }
#include <ardubus.h>

void setup()
{
    Serial.begin(115200);
    // Set some I2C values that should not be set automagically by the library
    ardubus_setup();
    Serial.println("IM: suovula_gauge_servos");
    Serial.println("Booted");
}

void loop()
{
    ardubus_update();
}
