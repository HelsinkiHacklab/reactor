// Get this from http://dsscircuits.com/articles/arduino-i2c-master-library.html
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h>

// Container for the device
pca9635 driver;

void setup()
{
    Serial.begin(115200);
    // Set device address and call Wire.begin() (note: fake addesss)
    driver.begin(0xfe, true);
    Serial.println("Booted");
}

void loop()
{
    // Dump device registers and wait 15sek
    driver.dump_registers(0x0, 0x1b);
    delay(15000);
}
