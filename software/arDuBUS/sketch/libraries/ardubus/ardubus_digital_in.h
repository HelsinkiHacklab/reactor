#ifndef ardubus_digital_in_h
#define ardubus_digital_in_h
#include <WProgram.h> 
#include <Bounce.h>
#ifndef ARDUBUS_DIGITAL_IN_DEBOUNCE_TIME
#define ARDUBUS_DIGITAL_IN_DEBOUNCE_TIME 20 // milliseconds, see Bounce library
#endif
#ifndef ARDUBUS_DIGITAL_IN_DEBOUNCE_UPDATE_TIME
#define ARDUBUS_DIGITAL_IN_DEBOUNCE_UPDATE_TIME 5 // Milliseconds, how often to call update() on the deardubus_digital_in_bouncers, see Bounce library
#endif



// Enumerate the input pins from the preprocessor
const byte ardubus_digital_in_pins[] = ARDUBUS_DIGITAL_INPUTS; 
// Declare and fake-initialize a debouncer for each
Bounce ardubus_digital_in_bouncers[sizeof(ardubus_digital_in_pins)] = Bounce(ardubus_digital_in_pins[0], ARDUBUS_DIGITAL_IN_DEBOUNCE_TIME); // We must initialize these here or things break, will overwrite with new instances in setup()


inline void ardubus_digital_in_setup()
{
    // Setup the deardubus_digital_in_bouncers
    for (byte i=0; i < sizeof(ardubus_digital_in_pins); i++)
    {
        pinMode(ardubus_digital_in_pins[i], INPUT);
        if (ardubus_digital_in_pins[i] != 13)
        {
            digitalWrite(ardubus_digital_in_pins[i], HIGH); // enable internal pull-up (except for #13 which has the led and external resistor, which will cause issues, see http://www.arduino.cc/en/Tutorial/DigitalPins)
        }
        ardubus_digital_in_bouncers[i] = Bounce(ardubus_digital_in_pins[i], ARDUBUS_DIGITAL_IN_DEBOUNCE_TIME);
    }
}

// Calls update method on all of the digital inputs and outputs message to Serial if state changed
unsigned long ardubus_digital_in_last_debounce_time;
inline void ardubus_digital_in_update_bouncers()
{
    // Update debouncer states
    for (byte i=0; i < sizeof(ardubus_digital_in_pins); i++)
    {
        if (ardubus_digital_in_bouncers[i].update())
        {
            // State changed
            Serial.print("CD"); // CD<pin_byte><state_byte>
            // PONDER: Use index instead of pin-number ?
            Serial.print(ardubus_digital_in_pins[i]);
            Serial.println(ardubus_digital_in_bouncers[i].read());
        }
    }
    ardubus_digital_in_last_debounce_time = millis();
}

inline void ardubus_digital_in_update()
{
    if ((millis() - ardubus_digital_in_last_debounce_time) > ARDUBUS_DIGITAL_IN_DEBOUNCE_UPDATE_TIME)
    {
        ardubus_digital_in_update_bouncers();
    }
}

inline void ardubus_digital_in_report()
{
    for (byte i=0; i < sizeof(ardubus_digital_in_pins); i++)
    {
        Serial.print("RD"); // RD<pin_byte><state_byte><time_long_as_hex>
        // PONDER: Use index instead of pin-number ?
        Serial.print(ardubus_digital_in_pins[i]);
        Serial.print(ardubus_digital_in_bouncers[i].read());
        // This might not be the best way to pass this info, maybe fixed-lenght encoding would be better ?
        Serial.println(ardubus_digital_in_bouncers[i].duration(), HEX);
    }
}

inline void ardubus_digital_in_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x44: // ASCII "D" (D<pinbyte><statebyte>) //The pin must have been declared in d_output_pins or unexpected things will happen
            if (incoming_command[2] == 0x31) // ASCII "1"
            {
                digitalWrite(incoming_command[1]-ARDUBUS_INDEX_OFFSET, HIGH);
            }
            else
            {
                digitalWrite(incoming_command[1]-ARDUBUS_INDEX_OFFSET, LOW);
            }
            Serial.print("D");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6); // ACK
            break;
    }
}


#endif
// *********** END OF CODE **********
