#ifndef ardubus_pca9535_out_h
#define ardubus_pca9535_out_h
#include <Arduino.h> 
#include "ardubus_pca9535_common.h"
#include <pca9535.h>

// Enumerate the input pins from the preprocessor (from pin numbers 0 to N, will run across the ARDUBUS_PCA9535_BOARDS array [so pin 16 is portA pin 0 on index 1 of ardubus_pca9535_boards])
const byte ardubus_pca9535_out_pins[] = ARDUBUS_PCA9535_OUTPUTS; 

inline void ardubus_pca9535_out_setup()
{
    for (byte i=0; i < sizeof(ardubus_pca9535_out_pins); i++)
    {
        ardubus_pca9535s[ardubus_pca9535_pin2board_idx(ardubus_pca9535_in_pins[i])].pinMode((ardubus_pca9535_out_pins[i] % 16), OUTPUT);
        /**
         * This is the default and doing N writes is not exactly optimal even if we do it only once
        ardubus_pca9535s[ardubus_pca9535_pin2board_idx(ardubus_pca9535_in_pins[i])].digitalWrite((ardubus_pca9535_in_pins[i] % 16), LOW);
         */
    }
}

inline void ardubus_pca9535_out_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_pca9535_out_report()
{
    // PONDER: Do we need to report back the last value set and when it was set ??
}

inline void ardubus_pca9535_out_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x45: // ASCII "E" (D<pinbyte><statebyte>) //The pin must have been declared in ardubus_pca9535_out_pins or unexpected things will happen
            byte pin = ardubus_pca9535_out_pins[incoming_command[1]-ARDUBUS_INDEX_OFFSET];
            if (incoming_command[2] == 0x31) // ASCII "1"
            {
                ardubus_pca9535s[ardubus_pca9535_pin2board_idx(pin)].digitalWrite((pin % 16), HIGH);
            }
            else
            {
                ardubus_pca9535s[ardubus_pca9535_pin2board_idx(pin)].digitalWrite((pin % 16), LOW);
            }
            Serial.print("E");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            ardubus_ack();
            break;
    }
}


#endif
// *********** END OF CODE **********
