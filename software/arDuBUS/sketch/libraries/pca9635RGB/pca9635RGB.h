// safety againts double-include
#ifndef pca9635RGB_h
#define pca9635RGB_h
#include <WProgram.h> 
#include <pca9635.h>

class pca9635RGB
{
    public:
        pca9635RGB();
        ~pca9635RGB();
        // Initialize the object and chip        
        void begin(byte board_addr, boolean wire_begin);
        // A funky way to handle optional arguments
        void begin(byte board_addr);
        void begin();
        // Color channel instances, allow public access for debugging
        pca9635 R;
        pca9635 G;
        pca9635 B;
        
};

#endif
// *********** END OF CODE **********
