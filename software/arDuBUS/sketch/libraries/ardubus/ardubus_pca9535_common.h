#ifndef ardubus_pca9535_common_h
#define ardubus_pca9535_common_h
#include <pca9535.h>

const byte ardubus_pca9535_boards[] = ARDUBUS_PCA9535_BOARDS;
// Declare a Servo object for each
pca9535 ardubus_pca9535s[sizeof(ardubus_pca9535_boards)];

inline byte ardubus_pca9535_pin2board_idx(byte pin)
{
    return pin/16;
}

inline void ardubus_pca9535_common_setup()
{
    // Setup the boards
    for (byte i=0; i < sizeof(ardubus_pca9535_boards); i++)
    {
        ardubus_pca9535s[i].begin(ardubus_pca9535_boards[i], false);
    }
}

#endif