#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15 }
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_PCA9535_BOARDS { 0 }
#define PCA9535_ENABLE_BOUNCE
#define PCA9535_BOUNCE_OPTIMIZEDREADS
#define ARDUBUS_PCA9535_INPUTS { 0, 1, 2, 3, 4, 5, 6, 7 }
#define ARDUBUS_PCA9535_OUTPUTS { 8, 9, 10, 11, 12, 13, 14, 15 }
#include <pca9535.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGB.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGBJBOL.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_PCA9635RGBJBOL_BOARDS { 0, 1 }
#define ARDUBUS_AIRCORE_BOARDS { 4, 5, 6, 7, 8 }

#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    Serial.println(F(""));
    Serial.println(F("Board: rod_control_panel initializing"));
    
    I2c.timeOut(500); // 500ms timeout to avoid lockups
    I2c.pullup(false); //Disable internal pull-ups
    I2c.setSpeed(false); // Fast-mode support
    ardubus_setup();
    PCA9635.set_driver_mode(0x0);
    PCA9635.set_sleep(0x0);
    Serial.println(F("Board: rod_control_panel ready"));
}

void loop()
{
    ardubus_update();
}
