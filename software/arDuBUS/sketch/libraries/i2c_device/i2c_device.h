// safety againts double-include
#ifndef i2c_device_h
#define i2c_device_h
#include <Arduino.h> 
// Defined here for now due to a problem with scope
#define I2C_DEVICE_DEBUG
/**
 * Superceded byt the I2C master library
#include <Wire.h>
 */
#include <I2C.h> // Get it from http://github.com/rambo/I2C

class i2c_device
{
    public:
        void begin(uint8_t dev_addr, uint8_t wire_begin);

        // A Very shorthand helper for reading single uint8_t (NOTE: does not do error-checking!)
        uint8_t read(byte address);
        // Read single uint8_t to a referred target (calls read_many internally)
        uint8_t read(uint8_t address, byte *target);
        // Read N uint8_ts to a target (usually an array)
        uint8_t read_many(uint8_t address, byte num, byte *target);
        // Helper to write a single uint8_t value (calls write_many internally)
        uint8_t write(uint8_t address, byte value);
        // Write N values from a source (usually an array)
        uint8_t write_many(uint8_t address, byte num, byte *source);
        // Do a masked read/modify/write operation to an address (defaults to ORing the value)
        uint8_t read_modify_write(uint8_t address, byte mask, byte value);
        // Do a masked read/modify/write operation to an address
        uint8_t read_modify_write(uint8_t address, byte mask, byte value, byte operand);
        // Helper to debug state, dumps given register values
        void dump_registers(uint8_t addr_start, byte addr_end);

    protected:
        uint8_t device_address;
};


#endif
// *********** END OF CODE **********
