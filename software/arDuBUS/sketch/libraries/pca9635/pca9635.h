// safety againts double-include
#ifndef pca9635_h
#define pca9635_h
#include <WProgram.h> 
// Defined here for now due to a problem with scope
#define I2C_DEVICE_DEBUG
#include <i2c_device.h>

// Stub extension for now
class pca9635 : public i2c_device
{
    public:
        pca9635();
        ~pca9635();
        
        boolean set_led_mode(byte ledno, byte mode);
        boolean set_led_mode(byte mode); // Variant to set all leds to same mode
        boolean set_led_pwm(byte ledno, byte cycle);
        boolean set_driver_mode(byte mode);
        boolean set_sleep(byte sleep);
        boolean reset(); // NOTE: This resets all PCA9635 devices on the bus
};

#endif
// *********** END OF CODE **********
