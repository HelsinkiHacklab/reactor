#include "i2c_device.h"

void i2c_device::begin(uint8_t dev_addr, uint8_t wire_begin)
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

uint8_t i2c_device::read(uint8_t address, byte *target)
{
    return this->read_many(address, 1, target);
}
uint8_t i2c_device::read(byte address)
{
    uint8_t target;
    this->read_many(address, 1, &target);
    return target;
}

uint8_t i2c_device::read_many(uint8_t address, byte req_num, byte *target)
{
    uint8_t result = I2c.read(device_address, address, req_num, target);
    if (result > 0)
    {
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Read ");
        Serial.print(req_num, DEC);
        Serial.print(" uint8_ts from dev 0x");
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
 * Write a single uint8_t and check the result
 */
uint8_t i2c_device::write(uint8_t address, byte value)
{
    uint8_t result = I2c.write(device_address, address, value);
    if (result > 0)
    {
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Writing value 0x ");
        Serial.print(value, HEX);
        Serial.print(" uint8_ts to dev 0x");
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
 * Write multiple uint8_ts and check result
 */
uint8_t i2c_device::write_many(uint8_t address, byte num, byte *source)
{
    uint8_t result = I2c.write(device_address, address, source, num);
    if (result > 0)
    {
#ifdef I2C_DEVICE_DEBUG
        Serial.print("DEBUG: Write ");
        Serial.print(num, DEC);
        Serial.print(" uint8_ts to dev 0x");
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
uint8_t i2c_device::read_modify_write(uint8_t address, byte mask, byte value, byte operand)
{
    uint8_t tmp;
    if (!this->read_many(address, 1, &tmp))
    {
        return false;
    }
/*
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
*/
    // TODO: These need a re-think, basically: how to set the masked bits to the values in the value uint8_t
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
/*
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
*/
    return this->write_many(address, 1, &tmp);
}

uint8_t i2c_device::read_modify_write(uint8_t address, byte mask, byte value)
{
    return this->read_modify_write(address, mask, value, 0);
}

/**
 * This does the reg dumping the naive way just in case the
 * usually supposed-to-be-present register autoincrement does not work as
 * expected
 */
void i2c_device::dump_registers(uint8_t addr_start, byte addr_end)
{
    uint8_t tmp;
    for (uint8_t addr = addr_start; addr <= addr_end; addr++)
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





