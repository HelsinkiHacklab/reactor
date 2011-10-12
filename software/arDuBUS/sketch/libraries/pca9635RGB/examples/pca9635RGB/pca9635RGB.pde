/**
 * Remember your I2C pull-up resistors
 */
#define I2C_DEVICE_DEBUG
#include <Wire.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGB.h>

// Container for the device
pca9635RGB driverboard;

void setup()
{
    Serial.begin(115200);
    // Set device address and call Wire.begin() (note: fake addesss)
    driverboard.begin(8);
    Serial.println("Booted");
}

void loop()
{
    // Dump device registers and wait 15sek
    Serial.println("Calling driverboard.R.dump_registers(0x0, 0x1b)");
    driverboard.R.dump_registers(0x0, 0x1b);
    Serial.println("Calling driverboard.G.dump_registers(0x0, 0x1b)");
    driverboard.G.dump_registers(0x0, 0x1b);
    Serial.println("Calling driverboard.B.dump_registers(0x0, 0x1b)");
    driverboard.B.dump_registers(0x0, 0x1b);
    delay(15000);
}
