#ifndef ardubus_aircore_h
#define ardubus_aircore_h
#include <Arduino.h> 
#include <i2c_device.h>

// Enumerate the aircore pins from the preprocessor
const byte ardubus_aircore_boards[] = ARDUBUS_AIRCORE_BOARDS;
// Declare a Servo object for each
i2c_device ardubus_aircores[sizeof(ardubus_aircore_boards)];

inline void ardubus_aircore_setup()
{
    I2c.begin();
    for (byte i=0; i < sizeof(ardubus_aircore_boards); i++)
    {
        ardubus_aircores[i].begin(ardubus_aircore_boards[i], false);
    }
}

inline void ardubus_aircore_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_aircore_report()
{
    // TODO: Do we want reports of led states ?
}

inline void ardubus_aircore_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x41: // ASCII "A" (A<indexbyte><motorbyte><value>) //Note that the indexbyte is index of the aircores-array, not pin number, ledbyte is the number of the led on the board
            ardubus_aircores[incoming_command[1]-ARDUBUS_INDEX_OFFSET].write(incoming_command[2]-ARDUBUS_INDEX_OFFSET, incoming_command[3]);
            Serial.print(F("A"));
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.print(incoming_command[3]);
            ardubus_ack();
            break;
    }
}

#endif
// *********** END OF CODE **********
