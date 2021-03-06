/**
 * TODO: Document
 *
 * Pin 10 Is used as the latch output (it must be output since SPI library will go to slave otherwise and we need latch anyway)
 * Pin 11 is the data line (MOSI in SPI terms)
 * Pin 12 (probably?) must be input (MISO in SPI terms) (and in this case it's useless to us since SPI library will clock arbitrary data in) due to the SPI library, though it might be possible to use it as output.caveat emptor
 * Pin 13 is the clock line
 * Reset is optional, tie it high on 595 if you don't want to use it (define ARDUBUS_SPI74XX595_RESETPIN to use)
 * Output-enable(active-low) is optional, tie it to ground if you don't want to use it (use ardubus_digital_out to control OE- if you wish)
 */
#include <SPI.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_SPI74XX595_INITVALUE 0xff // Initial value to set to registers on setup 
#define ARDUBUS_SPI74XX595_REGISTER_COUNT 9 // How many 595 registers do you have
//#define ARDUBUS_SPI74XX595_RESETPIN 9 // Use this pin for reset, optional but recommended
#define ARDUBUS_SPI74XX595_SPICLOCKDIV SPI_CLOCK_DIV64
#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    /**
     * Test ASCII-HEX to byte conversions
    for (byte i=0x30; i<0x3a; i++)
    {
        Serial.println(ardubus_hex2byte(i), DEC);
    }
    for (byte i=0x41; i<0x47; i++)
    {
        Serial.println(ardubus_hex2byte(i), DEC);
    }
    Serial.println(ardubus_hex2byte(0x30, 0x30), DEC); // 00
    Serial.println(ardubus_hex2byte(0x46, 0x46), DEC); // FF
    Serial.println(ardubus_hex2byte(0x41, 0x35), DEC); // A5
     */
    ardubus_setup();
    Serial.println(F("Booted"));
}

void set_bit(byte bit_index, boolean bit_dir)
{
      byte bit_value;
      byte bit_pos = 7-(bit_index%8);
      byte reg_index = bit_index/8;
      byte mask = (byte)~_BV(bit_pos);
      if (bit_dir) // ASCII "1"
      {
          bit_value = (byte)_BV(bit_pos); // Raise the correct bit
      }
      else
      {
          bit_value = 0x0; // Make all bits low
      }
      // Set only the given bit in the correct register
      ardubus_spi74XX595_values[reg_index] = (ardubus_spi74XX595_values[reg_index] & mask) | bit_value;
}

void loop()
{
    for (byte i=0; i<(ARDUBUS_SPI74XX595_REGISTER_COUNT*8); i++)
    {
         if (i>0)
         {
             set_bit(i-1, true);
         }
         /*
         Serial.print(F("i="));
         Serial.println(i, DEC);
         */
         set_bit(i, false);
         ardubus_spi74XX595_write();
         delay(250);
    }
}
