#ifndef ardubus_spi74XX595_h
#define ardubus_spi74XX595_h
#include <WProgram.h> 
#include <SPI.h>

#define ARDUBUS_SPI74XX595_LATCHPIN 10

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
    for (byte d=ARDUBUS_SPI74XX595_REGISTER_COUNT; d>0; d--)
    {
        SPI.transfer(ardubus_spi74XX595_values[d]);
    }
    digitalWrite(ARDUBUS_SPI74XX595_LATCHPIN, HIGH);
}


inline void ardubus_spi74XX595_setup()
{
    SPI.begin();
    SPI.setDataMode(SPI_MODE1);
    SPI.setBitOrder(LSBFIRST);
    SPI.setClockDivider(SPI_CLOCK_DIV4); // This should still work with messy cables
    ardubus_spi74XX595_reset();
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
            boolean bit_value;
            if (incoming_command[2] == 0x31) // ASCII "1"
            {
                bit_value = 0x0;
            }
            else
            {
                bit_value = 0xff;
            }
            byte bit_index = incoming_command[1]-ARDUBUS_INDEX_OFFSET;
            byte bit_pos = 7-(i%8);
            byte reg_index = bit_index/8;
            // Set only the given bit in the correct register
            ardubus_spi74XX595_values[reg_index] = (ardubus_spi74XX595_values[reg_index] & ~_BV(bit_pos)) | bit_value;
            ardubus_spi74XX595_write();
            Serial.print("B");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6); // ACK
            break;
        }
    }
}




#endif
// *********** END OF CODE **********
