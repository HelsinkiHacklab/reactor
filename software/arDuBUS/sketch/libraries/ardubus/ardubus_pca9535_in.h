#ifndef ardubus_pca9535_in_h
#define ardubus_pca9535_in_h
#include <Arduino.h> 
#define PCA9535_ENABLE_BOUNCE
#define PCA9535_BOUNCE_OPTIMIZEDREADS // Do not use the naive methods that will always read the device, handy when you have multiple pins to debounce, OTOH you must remember to call the read_data() method yourself
#include "ardubus_pca9535_common.h"
#include <pca9535.h>
#ifndef ARDUBUS_PCA9535_IN_DEBOUNCE_TIME
#define ARDUBUS_PCA9535_IN_DEBOUNCE_TIME 20 // milliseconds, see Bounce library
#endif
#ifndef ARDUBUS_PCA9535_IN_DEBOUNCE_UPDATE_TIME
#define ARDUBUS_PCA9535_IN_DEBOUNCE_UPDATE_TIME 5 // Milliseconds, how often to call update() on the deardubus_pca9535_in_bouncers, see Bounce library
#endif

// Enumerate the input pins from the preprocessor (from pin numbers 0 to N, will run across the ARDUBUS_PCA9535_BOARDS array [so pin 16 is portA pin 0 on index 1 of ardubus_pca9535_boards])
const byte ardubus_pca9535_in_pins[] = ARDUBUS_PCA9535_INPUTS; 
// Declare and fake-initialize a debouncer for each
pca9535bounce ardubus_pca9535_in_bouncers[sizeof(ardubus_pca9535_in_pins)];

inline void ardubus_pca9535_in_setup()
{
    // Setup the debouncers
    for (byte i=0; i < sizeof(ardubus_pca9535_in_pins); i++)
    {
        ardubus_pca9535s[ardubus_pca9535_pin2board_idx(ardubus_pca9535_in_pins[i])].pinMode((ardubus_pca9535_in_pins[i] % 16), INPUT);
        ardubus_pca9535_in_bouncers[i].begin(&ardubus_pca9535s[ardubus_pca9535_pin2board_idx(ardubus_pca9535_in_pins[i])], (ardubus_pca9535_in_pins[i] % 16), ARDUBUS_PCA9535_IN_DEBOUNCE_TIME);
    }
}

// Calls update method on all of the digital inputs and outputs message to Serial if state changed
unsigned long ardubus_pca9535_in_last_debounce_time;
inline void ardubus_pca9535_in_update_bouncers()
{
    // Read data
    for (byte i=0; i < sizeof(ardubus_pca9535_boards); i++)
    {
        ardubus_pca9535s[i].read_data();
    }
    // Update debouncer states
    for (byte i=0; i < sizeof(ardubus_pca9535_in_pins); i++)
    {
        if (ardubus_pca9535_in_bouncers[i].update())
        {
            // State changed
            Serial.print(F("CP")); // CD<index_byte><state_byte>
            Serial.write(i);
            Serial.println(ardubus_pca9535_in_bouncers[i].read());
        }
    }
    ardubus_pca9535_in_last_debounce_time = millis();
}

inline void ardubus_pca9535_in_update()
{
    if ((millis() - ardubus_pca9535_in_last_debounce_time) > ARDUBUS_PCA9535_IN_DEBOUNCE_UPDATE_TIME)
    {
        ardubus_pca9535_in_update_bouncers();
    }
}

inline void ardubus_pca9535_in_report()
{
    for (byte i=0; i < sizeof(ardubus_pca9535_in_pins); i++)
    {
        Serial.print(F("RP")); // RD<index_byte><state_byte><time_long_as_hex>
        Serial.write(i);
        Serial.print(ardubus_pca9535_in_bouncers[i].read());
        ardubus_print_ulong_as_8hex(ardubus_pca9535_in_bouncers[i].duration());
        Serial.println(F(""));
    }
}

inline void ardubus_pca9535_in_process_command(char *incoming_command)
{
    // This is a no-op (but defined so that all submodules have same API)
}


#endif
// *********** END OF CODE **********
