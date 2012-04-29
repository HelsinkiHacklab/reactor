#ifndef ardubus_spi74XX595_h
#define ardubus_spi74XX595_h
#include <Arduino.h> 
#include <SPI.h>
#ifndef ARDUBUS_SPI74XX595_SPICLOCKDIV
#define ARDUBUS_SPI74XX595_SPICLOCKDIV SPI_CLOCK_DIV16
#endif
#ifndef ARDUBUS_SPI74XX595_INITVALUE
#define ARDUBUS_SPI74XX595_INITVALUE 0x0
#endif

/**
 * Reminder
 * SS = 10 (aka CS aka latch) we could use another one but there are caveats
 * MOSI = 11 (aka serial out)
 * MISO = 12 (not used)
 * SCLK = 13
 */
#ifndef ARDUBUS_SPI74XX595_LATCHPIN
#define ARDUBUS_SPI74XX595_LATCHPIN 10 //SPI default SS according to http://arduino.cc/en/Reference/SPI
#endif

byte ardubus_spi74XX595_values[ARDUBUS_SPI74XX595_REGISTER_COUNT];

inline void ardubus_spi74XX595_reset()
{
#ifdef ARDUBUS_SPI74XX595_RESETPIN
    digitalWrite(ARDUBUS_SPI74XX595_RESETPIN, LOW);
    delayMicroseconds(1);
    digitalWrite(ARDUBUS_SPI74XX595_RESETPIN, HIGH);
#endif
}

inline void ardubus_spi74XX595_write()
{
    ardubus_spi74XX595_reset();
    digitalWrite(ARDUBUS_SPI74XX595_LATCHPIN, LOW);
    for (byte i=0; i<ARDUBUS_SPI74XX595_REGISTER_COUNT; i++)
    {
        byte reg = (ARDUBUS_SPI74XX595_REGISTER_COUNT-1)-i;
        SPI.transfer(ardubus_spi74XX595_values[reg]);
        /*
        Serial.print("DEBUG: wrote ardubus_spi74XX595_values[");
        Serial.print(reg, DEC);
        Serial.print("] value B");
        Serial.println(ardubus_spi74XX595_values[reg], BIN);
        */
    }
    digitalWrite(ARDUBUS_SPI74XX595_LATCHPIN, HIGH);
}


inline void ardubus_spi74XX595_setup()
{
    SPI.begin();
    // Expirementing with modes, I got this working with bus pirate using SPI at 1Mhz for now it somehow fails ??
    SPI.setDataMode(SPI_MODE0);
    //SPI.setDataMode(SPI_MODE1);
    //SPI.setDataMode(SPI_MODE2);
    //SPI.setDataMode(SPI_MODE3);
    //SPI.setBitOrder(LSBFIRST);
    SPI.setBitOrder(MSBFIRST);
    SPI.setClockDivider(ARDUBUS_SPI74XX595_SPICLOCKDIV); // This should still work with messy cables
    for (byte i=0; i<ARDUBUS_SPI74XX595_REGISTER_COUNT; i++)
    {
        ardubus_spi74XX595_values[(ARDUBUS_SPI74XX595_REGISTER_COUNT-1)-i] = ARDUBUS_SPI74XX595_INITVALUE;
    }
    if (ARDUBUS_SPI74XX595_LATCHPIN != 10)
    {
        pinMode(10, OUTPUT); // The SS pin *must* be output in any case!! see http://arduino.cc/en/Reference/SPI
    }
    pinMode(ARDUBUS_SPI74XX595_LATCHPIN, OUTPUT);
    digitalWrite(ARDUBUS_SPI74XX595_LATCHPIN, HIGH);
#ifdef ARDUBUS_SPI74XX595_RESETPIN
    pinMode(ARDUBUS_SPI74XX595_RESETPIN, OUTPUT);
    digitalWrite(ARDUBUS_SPI74XX595_RESETPIN, HIGH);
#endif
    ardubus_spi74XX595_write();
}

inline void ardubus_spi74XX595_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_spi74XX595_report()
{
    // TODO: Do we want reports of the register states ?
}

inline void ardubus_spi74XX595_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x42: // ASCII "B" (B<indexbyte><value>) //Note that the indexbyte is index of the bit
        {
            byte bit_value;
            // TODO: Can the compiler optimize all this or do I need to write oneliners ?
            byte bit_index = incoming_command[1]-ARDUBUS_INDEX_OFFSET;
            byte bit_pos = 7-(bit_index%8);
            byte reg_index = bit_index/8;
            byte mask = (byte)~_BV(bit_pos);
            if (incoming_command[2] == 0x31) // ASCII "1"
            {
                bit_value = (byte)_BV(bit_pos); // Raise the correct bit
            }
            else
            {
                bit_value = 0x0; // Make all bits low
            }
            // Set only the given bit in the correct register
            ardubus_spi74XX595_values[reg_index] = (ardubus_spi74XX595_values[reg_index] & mask) | bit_value;
            ardubus_spi74XX595_write();
            Serial.print("B");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            //Serial.println(0x6, BYTE); // ACK
            break;
        }
        case 0x57: // ASCII "W" (B<indexbyte><valuehex>) //Note that the indexbyte is index of register, value is two hex chars
        {
            byte reg_index = incoming_command[1]-ARDUBUS_INDEX_OFFSET;
            ardubus_spi74XX595_values[reg_index] = ardubus_hex2byte(incoming_command[2], incoming_command[3]);
            ardubus_spi74XX595_write();
            Serial.print("W");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.print(incoming_command[3]);
            //Serial.println(0x6, BYTE); // ACK
            break;
        }
    }
}




#endif
// *********** END OF CODE **********
