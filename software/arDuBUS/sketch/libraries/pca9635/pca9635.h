// safety againts double-include
#ifndef pca9635_h
#define pca9635_h
#include <WProgram.h> 
#include <i2c_device.h>

// Stub extension for now
class pca9635 : public i2c_device
{
    public:
        pca9635();
        ~pca9635();
};


#endif
// *********** END OF CODE **********
