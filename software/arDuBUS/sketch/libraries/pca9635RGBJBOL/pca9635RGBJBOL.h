// safety againts double-include
#ifndef pca9635RGBJBOL_h
#define pca9635RGBJBOL_h
#include <WProgram.h> 
#include <pca9635RGB.h>

class pca9635RGBJBOL : public pca9635RGB
{
    public:
        // Proxies to all the individual drivers
        boolean set_led_pwm(byte ledno, byte cycle);
        boolean set_led_mode(byte ledno, byte mode);
        boolean set_led_mode(byte mode); 
        boolean set_driver_mode(byte mode);
        boolean set_sleep(byte sleep);
};

#endif
// *********** END OF CODE **********
