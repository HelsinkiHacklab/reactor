// safety againts double-include
#ifndef pca9635RGBJBOL_h
#define pca9635RGBJBOL_h
#include <Arduino.h> 
#include <pca9635RGB.h>

class pca9635RGBJBOL : public pca9635RGB
{
    public:
        // Proxies to all the individual drivers
        uint8_t set_led_pwm(uint8_t ledno, byte cycle);
        uint8_t set_led_mode(uint8_t ledno, byte mode);
        uint8_t set_led_mode(uint8_t mode); 
        uint8_t set_driver_mode(uint8_t mode);
        uint8_t set_sleep(uint8_t sleep);
};

#endif
// *********** END OF CODE **********
