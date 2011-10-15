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
    PCA9635.reset(); // This should reset all drivers on the bus
    PCA9635.set_sleep(0x0); // Wake up oscillators (via all-call)
    delayMicroseconds(500); // Wait for the oscillators to stabilize
    // Initialize the pca9635 instances with correct addresses
    R.begin(board_num | (0x1 << 5), false, false);
    G.begin(board_num | (0x2 << 5), false, false);
    B.begin(board_num | (0x3 << 5), false, false);
    R.enable_subddr(1);
    G.enable_subddr(2);
    B.enable_subddr(3);
    PCA9635.set_driver_mode(0x0); // Default to open-drain mode for all drivers (via all-call)
    PCA9635.set_led_mode(3); // Default to PWM mode for all drivers (via all-call)
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

boolean pca9635RGB::set_rgb(byte ledno, byte rcycle, byte gcycle, byte bcycle)
{
    // TODO: When I2C library allows lower level access write as single repeated-start sequence for atomicity
    boolean rstat = R.set_led_pwm(ledno, rcycle);
    boolean gstat = G.set_led_pwm(ledno, gcycle);
    boolean bstat = B.set_led_pwm(ledno, bcycle);
    return rstat && gstat && bstat;
}

/*
pca9635::set_led_pwm(byte ledno, byte cycle)
{

*/
