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

        void begin(uint8_t dev_addr, uint8_t wire_begin);
        void begin(uint8_t dev_addr, uint8_t wire_begin, boolean init); // Variant to allow skipiing init (needed by the RGB board)
        uint8_t set_led_mode(uint8_t ledno, byte mode);
        uint8_t set_led_mode(uint8_t mode); // Variant to set all leds to same mode
        uint8_t set_led_pwm(uint8_t ledno, byte cycle);
        uint8_t set_driver_mode(uint8_t mode);
        uint8_t set_sleep(uint8_t sleep);
        uint8_t enable_subaddr(uint8_t addr);
        uint8_t reset(); // NOTE: This resets all PCA9635 devices on the bus
        uint8_t autoincrement_bits;
};

extern pca9635 PCA9635;


#endif
// *********** END OF CODE **********
