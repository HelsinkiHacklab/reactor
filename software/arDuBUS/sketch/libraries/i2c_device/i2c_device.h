// safety againts double-include
#ifndef i2c_device_h
#define i2c_device_h
#include <WProgram.h> 
#include <Wire.h>


class i2c_device
{
    public:
        i2c_device();
        ~i2c_device();
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
        // Do a masked read/modify/write operation to an address
        boolean read_modify_write(byte address, byte mask, byte value);
        // Helper to debug state, dumps given register values
        void dump_registers(byte addr_start, byte addr_end);

    protected:
        byte device_address;
};


#endif
// *********** END OF CODE **********
