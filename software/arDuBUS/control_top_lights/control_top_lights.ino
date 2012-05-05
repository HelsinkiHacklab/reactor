#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#define I2C_DEVICE_DEBUG
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGB.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGBJBOL.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_PCA9635RGBJBOL_BOARDS { 0, 1 }

#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    // Set some I2C values that should not be set automagically by the library
    I2c.timeOut(500); // 500ms timeout to avoid lockups
    I2c.pullup(false); //Disable internal pull-ups
    I2c.setSpeed(true); // Fast-mode support
    
    I2c.scan();
    
    ardubus_setup();
    PCA9635.set_driver_mode(0x0);
    PCA9635.set_sleep(0x0);
    Serial.println("Booted");
}

void loop()
{
    ardubus_update();
    /*
    // Test code, blink each led once
    for (byte i = 0; i < 48; i++)
    {
        Serial.println(i, DEC);
        ardubus_pca9635RGBJBOLs[0].set_led_pwm(i, 255);
        delay(250);
        ardubus_pca9635RGBJBOLs[0].set_led_pwm(i, 0);
    }
    for (byte i = 0; i < 48; i++)
    {
        Serial.println(i, DEC);
        ardubus_pca9635RGBJBOLs[1].set_led_pwm(i, 255);
        delay(250);
        ardubus_pca9635RGBJBOLs[1].set_led_pwm(i, 0);
    }
    */
}
