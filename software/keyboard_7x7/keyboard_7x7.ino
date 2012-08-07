#define I2C_DEVICE_DEBUG
// Get this from https://github.com/rambo/I2C
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <mcp23017.h>
// Container for the device
mcp23017 expander;
// "debounce" the keys, actually we probably read them so slowly it doesn't matter but this offers key repeats as well
#include <dummybounce.h>
#define DUMMY_BNC_COUNT 49
#define DUMMY_BNC_DEBOUNCE_TIME 20
dummybounce dummybouncers[DUMMY_BNC_COUNT];

void setup()
{
    Serial.begin(115200);

    // Initialize the bouncers
    for (byte i=0; i < DUMMY_BNC_COUNT; i++)
    {
        dummybouncers[i].begin(DUMMY_BNC_DEBOUNCE_TIME);
    }

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

void scan_matrix()
{
    for (byte i=0; i < 7; i++)
    {
        scan_matrix_column(i);
    }
}

void scan_matrix_column(byte col)
{
    expander.data[0] = (expander.data[0] & B10000000) | (0x1 << col);
    expander.sync();
    
    /*
    Serial.print("expander.data[0] B");
    Serial.println(expander.data[0], BIN);
    Serial.print("expander.data[1] B");
    Serial.println(expander.data[1], BIN);
    */
    
    byte rowdata = expander.data[1] >> 1;
    for (byte row=0; row < 7; row++)
    {
        byte idx = (row*7)+col;
        if (_BV(row) & rowdata)
        {
            dummybouncers[idx].dummystate = HIGH;
        }
        else
        {
            dummybouncers[idx].dummystate = LOW;
        }
    }

}

void loop()
{
    scan_matrix();
    for (byte i=0; i < DUMMY_BNC_COUNT; i++)
    {
        if (dummybouncers[i].update())
        {
            // State changed
            Serial.print("Bouncer #"); // CD<index_byte><state_byte>
            Serial.print(i, DEC);
            Serial.print(" state is ");
            Serial.println(dummybouncers[i].read(), DEC);
        }
    }
}
