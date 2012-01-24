// safety againts double-include
#ifndef pca9635RGB_h
#define pca9635RGB_h
#include <Arduino.h> 
#include <pca9635.h>

class pca9635RGB
{
    public:
        // Initialize the object and chip        
        void begin(uint8_t board_num, uint8_t wire_begin);
        // A funky way to handle optional arguments
        void begin(uint8_t board_num);
        void begin();
        uint8_t set_rgb(uint8_t ledno, byte rcycle, byte gcycle, byte bcycle);
        // Color channel instances, allow public access for debugging
        pca9635 R;
        pca9635 G;
        pca9635 B;
        
};

#endif
// *********** END OF CODE **********
