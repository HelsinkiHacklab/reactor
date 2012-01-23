// Get this from http://dsscircuits.com/articles/arduino-i2c-master-library.html
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h>

// Container for the device
pca9635 driver;

void setup()
{
    Serial.begin(115200);
    // Use the SW-Reset address to reset all pca9635 ICs on the bus
    PCA9635.reset(); // Incidentally this global name is a pca9635 instance bound to the generla "all-call" address so it can be used to set global parameters
    // Set device address and call I2c.begin() (note: your need to change the address to correspond to your device)
    driver.begin(0xfe, true);
    Serial.println("Booted");
}

void loop()
{
    // Dump device registers and wait 15sek
    driver.dump_registers(0x0, 0x1b);
    delay(15000);
}
