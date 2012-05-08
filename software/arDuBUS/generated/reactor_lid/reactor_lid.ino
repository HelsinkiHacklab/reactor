#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS { 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, A15, A14, A13, A12, A11, A10, A9, A8, A7, A6, A5, A4 }
#define ARDUBUS_PWM_OUTPUTS { 13, 12, 11, 10, 9 }

#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    Serial.println("");
    Serial.println("Board: reactor_lid initializing");
    ardubus_setup();
    Serial.println("Board: reactor_lid ready");
}

void loop()
{
    ardubus_update();
}
