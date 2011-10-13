#include "pca9635RGB.h"

pca9635RGB::pca9635RGB()
{
}
pca9635RGB::~pca9635RGB()
{
}

/**
 * board_num is the number selected on the BCD rotary switch
 */
void pca9635RGB::begin(byte board_num, boolean wire_begin)
{
    if (wire_begin)
    {
        I2c.begin();
    }
    R.reset(); // This will reset all drivers on the bus
    // Initialize the pca9635 instances
    R.begin(board_num | (0x2 << 5), false);
    G.begin(board_num | (0x1 << 5), false);
    B.begin(board_num | (0x3 << 5), false);
    // Wake up the oscillators
    R.set_sleep(0);
    G.set_sleep(0);
    B.set_sleep(0);
    delayMicroseconds(500); // Wait for the oscillators to stabilize
}

// Funky way to handle default arguments
void pca9635RGB::begin(byte board_addr)
{
    pca9635RGB::begin(board_addr, true);
}

void pca9635RGB::begin()
{
    pca9635RGB::begin(0x0, true);
}
