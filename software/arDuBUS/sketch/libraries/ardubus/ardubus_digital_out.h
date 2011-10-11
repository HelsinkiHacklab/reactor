#ifndef ardubus_digital_out_h
#define ardubus_digital_out_h
#include <WProgram.h> 
const byte ardubus_digital_out_pins[] = ARDUBUS_DIGITAL_OUTPUTS; // Digital outputs


inline void ardubus_digital_out_setup()
{
    for (byte i=0; i < sizeof(ardubus_digital_out_pins); i++)
    {
        pinMode(ardubus_digital_out_pins[i], OUTPUT);
        digitalWrite(ardubus_digital_out_pins[i], LOW);
    }
}

inline void ardubus_digital_out_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_digital_out_report()
{
    // TODO: Implement
}

inline void ardubus_digital_out_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x44: // ASCII "D" (D<pinbyte><statebyte>) //The pin must have been declared in ardubus_digital_out_pins or unexpected things will happen
            // PONDER: Use index instead of pin-number ?
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
