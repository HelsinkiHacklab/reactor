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
#define ARDUBUS_SPI74XX595_REGISTER_COUNT 3 // How many 595 registers do you have
#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    ardubus_setup();
    Serial.println("Booted");
}

void loop()
{
    ardubus_update();
}
