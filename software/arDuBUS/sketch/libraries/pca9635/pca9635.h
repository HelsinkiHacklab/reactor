// safety againts double-include
#ifndef pca9635_h
#define pca9635_h
#include <Arduino.h> 
#include <i2c_device.h>

// Stub extension for now
class pca9635 : public i2c_device
{
    public:
        pca9635(); // We need this so we can set default address to the all-call one for the PCA9635 instance

        void begin(byte dev_addr, boolean wire_begin);
        void begin(byte dev_addr, boolean wire_begin, boolean init); // Variant to allow skipiing init (needed by the RGB board)
        boolean set_led_mode(byte ledno, byte mode);
        boolean set_led_mode(byte mode); // Variant to set all leds to same mode
        boolean set_led_pwm(byte ledno, byte cycle);
        boolean set_driver_mode(byte mode);
        boolean set_sleep(byte sleep);
        boolean enable_subaddr(byte addr);
        boolean reset(); // NOTE: This resets all PCA9635 devices on the bus
        byte autoincrement_bits;
};

extern pca9635 PCA9635;


#endif
// *********** END OF CODE **********
