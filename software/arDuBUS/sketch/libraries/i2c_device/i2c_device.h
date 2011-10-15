// safety againts double-include
#ifndef i2c_device_h
#define i2c_device_h
#include <WProgram.h> 
// Defined here for now due to a problem with scope
#define I2C_DEVICE_DEBUG
/**
 * Superceded byt the I2C master library
#include <Wire.h>
 */
#include <I2C.h> // Get it from http://dsscircuits.com/articles/arduino-i2c-master-library.html

class i2c_device
{
    public:
        void begin(byte dev_addr, boolean wire_begin);

        // A Very shorthand helper for reading single byte (NOTE: does not do error-checking!)
        byte read(byte address);
        // Read single byte to a referred target (calls read_many internally)
        boolean read(byte address, byte *target);
        // Read N bytes to a target (usually an array)
        boolean read_many(byte address, byte num, byte *target);
        // Helper to write a single byte value (calls write_many internally)
        boolean write(byte address, byte value);
        // Write N values from a source (usually an array)
        boolean write_many(byte address, byte num, byte *source);
        // Do a masked read/modify/write operation to an address (defaults to ORing the value)
        boolean read_modify_write(byte address, byte mask, byte value);
        // Do a masked read/modify/write operation to an address
        boolean read_modify_write(byte address, byte mask, byte value, byte operand);
        // Helper to debug state, dumps given register values
        void dump_registers(byte addr_start, byte addr_end);

    protected:
        byte device_address;
};


#endif
// *********** END OF CODE **********
