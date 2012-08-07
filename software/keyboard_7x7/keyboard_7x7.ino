#define I2C_DEVICE_DEBUG
// Get this from https://github.com/rambo/I2C
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <mcp23017.h>
// Container for the device
mcp23017 expander;

void setup()
{
    Serial.begin(115200);

    // Initialize I2C library manually
    I2c.begin();
    I2c.timeOut(500);
    I2c.pullup(true);

    // While strictly not neccessary for the 0th board it's good reminder    
    expander.begin(0x0, false);
    
    expander.set_port_mode(0, B00000000); // Port A for output, A7 is indicator
    expander.set_port_mode(1, B11111110); // Port B mostly for reading, one indicator led
    /**
     * The patterns for turning both leds on
    expander.data[0] = B10000000;
    expander.data[1] = B00000001; 
     */
    expander.data[0] = 0x0;
    expander.data[1] = 0x0; 
    expander.write_data();

    Serial.println("Booted");
}

byte scan_matrix_column(byte col)
{
    
}

void loop()
{

}
