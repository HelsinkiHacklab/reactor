#ifndef ardubus_pca9635RGBJBOL_h
#define ardubus_pca9635RGBJBOL_h
#include <Arduino.h> 
#include <pca9635RGBJBOL.h>

// Enumerate the pca9635RGBJBOL pins from the preprocessor
const byte ardubus_pca9635RGBJBOL_boards[] = ARDUBUS_PCA9635RGBJBOL_BOARDS;
// Declare a Servo object for each
pca9635RGBJBOL ardubus_pca9635RGBJBOLs[sizeof(ardubus_pca9635RGBJBOL_boards)] = pca9635RGBJBOL();

inline void ardubus_pca9635RGBJBOL_setup()
{
    I2c.begin();
    for (byte i=0; i < sizeof(ardubus_pca9635RGBJBOL_boards); i++)
    {
        ardubus_pca9635RGBJBOLs[i].begin(ardubus_pca9635RGBJBOL_boards[i], false);
    }
}

inline void ardubus_pca9635RGBJBOL_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_pca9635RGBJBOL_report()
{
    // TODO: Do we want reports of led states ?
}

inline void ardubus_pca9635RGBJBOL_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x4A: // ASCII "J" (J<indexbyte><ledbyte><value>) //Note that the indexbyte is index of the pca9635RGBJBOLs-array, not pin number, ledbyte is the number of the led on the board
            ardubus_pca9635RGBJBOLs[incoming_command[1]-ARDUBUS_INDEX_OFFSET].set_led_pwm(incoming_command[2]-ARDUBUS_INDEX_OFFSET, incoming_command[3]);
            Serial.print("J");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.print(incoming_command[3]);
            ardubus_ack();
            break;
    }
}

#endif
// *********** END OF CODE **********
