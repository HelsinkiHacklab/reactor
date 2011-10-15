#include "i2c_device.h"

// Constructor
i2c_device::i2c_device()
{
}

// Destructor
i2c_device::~i2c_device()
{
}

void i2c_device::begin(byte dev_addr, boolean wire_begin)
{
    device_address = dev_addr;
    if (wire_begin)
    {
        I2c.begin();
    }
}

// TODO: Add read and write methods that take pointer to an iterator function

// TODO: Re-write the simplified methods to take advantage of the features of the I2C library
// TODO: Re-write to check for status codes from the I2C library on each send.

boolean i2c_device::read(byte address, byte *target)
{
    return this->read_many(address, 1, target);
}
byte i2c_device::read(byte address)
{
    byte target;
    this->read_many(address, 1, &target);
    return target;
}

boolean i2c_device::read_many(byte address, byte req_num, byte *target)
{
    byte result = I2c.read(device_address, address, req_num, target);
    if (result > 0)
    {
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Read ");
        Serial.print(req_num, DEC);
        Serial.print(" bytes from dev 0x");
        Serial.print(device_address, HEX);
        Serial.print(" reg 0x");
        Serial.print(address, HEX);
        Serial.print(" failed, I2c.read returned: ");
        Serial.println(result, DEC);
#endif
        return false;
    }
    return true;
    /*
    I2c.beginTransmission(device_address);
    I2c.send(address);
    byte result = I2c.endTransmission();
    if (result > 0)
    {
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Read from ");
        Serial.print("dev 0x");
        Serial.print(device_address, HEX);
        Serial.print(" reg 0x");
        Serial.print(address, HEX);
        Serial.print(" failed, I2c.endTransmission returned: ");
        Serial.println(result, DEC);
#endif
        return false;
    }
    I2c.requestFrom(device_address, req_num);
    byte recv_num =  I2c.available();
    if (recv_num != req_num)
    {
        // Unexpected amount of data to be received, clear the buffers and return failure
        while (recv_num-- > 0)
        {
            I2c.receive();
        }
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Read from ");
        Serial.print("dev 0x");
        Serial.print(device_address, HEX);
        Serial.print(" reg 0x");
        Serial.print(address, HEX);
        Serial.println(" failed, unexpected amount of data");
#endif
        return false;
    }
    while(recv_num-- > 0)
    {
        // First assign the return of I2c.receive to where the pointer points to, then incement the pointer (so in next iteration we write to correct place)
        *(target++) = I2c.receive();
    }
    return true;
    */
}


boolean i2c_device::write(byte address, byte value)
{
    return this->write_many(address, 1, &value);
}

boolean i2c_device::write_many(byte address, byte num, byte *source)
{
    /**
     * Wire style
    I2c.beginTransmission(device_address);
    I2c.send(address);
    I2c.send(source, num);
    */
    byte result = I2c.write(device_address, address, source, num);
    if (result > 0)
    {
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Write ");
        Serial.print(num, DEC);
        Serial.print(" bytes to dev 0x");
        Serial.print(device_address, HEX);
        Serial.print(" reg 0x");
        Serial.print(address, HEX);
        Serial.print(" failed, I2c.read returned: ");
        Serial.println(result, DEC);
#endif
        return false;
    }
    return true;
}

/**
 * Performs a masked read-write-modify -cycle, remember that your mask should have 1 on the bits not to modify and 0 on the bits to modify
 * 
 * Operands:
 * 0=OR
 * 1=AND
 * 2=XOR
 *
 */
boolean i2c_device::read_modify_write(byte address, byte mask, byte value, byte operand)
{
    byte tmp;
    if (!this->read_many(address, 1, &tmp))
    {
        return false;
    }
#ifdef I2C_DEVICE_DEBUG
    Serial.print("dev 0x");
    Serial.print(device_address, HEX);
    Serial.print(" BEFORE: reg 0x");
    Serial.print(address, HEX);
    Serial.print(" value: 0x");
    Serial.print(tmp, HEX);
    Serial.print("\tB");
    Serial.println(tmp, BIN);
    Serial.print("MASK: B");
    Serial.print(mask, BIN);
    Serial.print("\tVALUE: B");
    Serial.println(value, BIN);
#endif
    // TODO: These need a re-think, basically: how to set the masked bits to the values in the value byte
    switch (operand)
    {
        case 0:
            tmp = (tmp & mask) | value;
            break;
        case 1:
            tmp = (tmp & mask) & value;
            break;
        case 2:
            tmp = (tmp & mask) ^ value;
            break;

    }
#ifdef I2C_DEVICE_DEBUG
    Serial.print("dev 0x");
    Serial.print(device_address, HEX);
    Serial.print(" AFTER: reg 0x");
    Serial.print(address, HEX);
    Serial.print(" value: 0x");
    Serial.print(tmp, HEX);
    Serial.print("\tB");
    Serial.println(tmp, BIN);
#endif
    return this->write_many(address, 1, &tmp);
}

boolean i2c_device::read_modify_write(byte address, byte mask, byte value)
{
    return this->read_modify_write(address, mask, value, 0);
}

/**
 * This does the reg dumping the naive way just in case the
 * usually supposed-to-be-present register autoincrement does not work as
 * expected
 */
void i2c_device::dump_registers(byte addr_start, byte addr_end)
{
    byte tmp;
    for (byte addr = addr_start; addr <= addr_end; addr++)
    {
        if (!i2c_device::read(addr, &tmp))
        {
            continue;
        }
        Serial.print("dev 0x");
        Serial.print(device_address, HEX);
        Serial.print(" reg 0x");
        Serial.print(addr, HEX);
        Serial.print(" value: 0x");
        Serial.print(tmp, HEX);
        Serial.print("\tB");
        Serial.println(tmp, BIN);
    }
}





