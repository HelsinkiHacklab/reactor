
#define ARDUBUS_PCA9535_INPUTS { 7, 15 }
#define ARDUBUS_PCA9535_OUTPUTS { 14 }
#define ARDUBUS_PCA9535_BOARDS { 0 }
#define PCA9535_ENABLE_BOUNCE
#define PCA9535_BOUNCE_OPTIMIZEDREADS // Do not use the naive methods that will always read the device, handy when you have multiple pins to debounce, OTOH you must remember to call the read_data() method yourself
#define I2C_DEVICE_DEBUG
// Get this from https://github.com/rambo/I2C
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
// Get this from https://github.com/rambo/pca9535
#include <pca9535.h> // For some weird reason including this in the relevant .h file does not work


#include <ardubus.h>
void setup()
{
    Serial.begin(115200);

    // Initialize I2C library manually
    I2c.begin();
    I2c.timeOut(500);
    I2c.pullup(true);

    ardubus_setup();
    Serial.println(F("Booted"));
}

void loop()
{
    ardubus_update();
}
