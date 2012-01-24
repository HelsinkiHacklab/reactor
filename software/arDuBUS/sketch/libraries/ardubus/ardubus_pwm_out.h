#ifndef ardubus_pwm_out_h
#define ardubus_pwm_out_h
#include <Arduino.h> 
const uint8_t ardubus_pwm_out_pins[] = ARDUBUS_PWM_OUTPUTS; // Digital outputs

inline void ardubus_pwm_out_setup()
{
    for (uint8_t i=0; i < sizeof(ardubus_pwm_out_pins); i++)
    {
        pinMode(ardubus_pwm_out_pins[i], OUTPUT);
        digitalWrite(ardubus_pwm_out_pins[i], LOW);
    }
}

inline void ardubus_pwm_out_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_pwm_out_report()
{
    // PONDER: Do we need to report back the last value set and when it was set ??
}

inline void ardubus_pwm_out_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x50: // ASCII "P" (P<pinuint8_t><cyclebyte>) //The pin must have been declared in d_output_pins or unexpected things will happen (and must support HW PWM)
            uint8_t pin = ardubus_pwm_out_pins[incoming_command[1]-ARDUBUS_INDEX_OFFSET];
            analogWrite(pin, incoming_command[2]);
            Serial.print("P");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6, BYTE); // ACK
            break;
    }
}

#endif
// *********** END OF CODE **********
