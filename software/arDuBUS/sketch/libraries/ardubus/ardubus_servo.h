#ifndef ardubus_servo_h
#define ardubus_servo_h
#include <Arduino.h> 
#include <Servo.h>

// Enumerate the servo pins from the preprocessor
const uint8_t ardubus_servo_output_pins[] = ARDUBUS_SERVO_OUTPUTS;
// Declare a Servo object for each
Servo ardubus_servos[sizeof(ardubus_servo_output_pins)] = Servo();

inline void ardubus_servo_setup()
{
    for (uint8_t i=0; i < sizeof(ardubus_servo_output_pins); i++)
    {
        ardubus_servos[i].attach(ardubus_servo_output_pins[i]);
        ardubus_servos[i].write(90);
    }
}

inline void ardubus_servo_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_servo_report()
{
    /**
     * Not used yet anywhere, also: convert to output 4 hex int
    for (uint8_t i=0; i < sizeof(ardubus_servo_output_pins); i++)
    {
        Serial.print("RS"); // RS<index_uint8_t><value in hex>
        Serial.print(i);
        ardubus_print_uint8_t_as_2hex(ardubus_servos[i].read());
        Serial.println("");
        // TODO: Keep track of duration ??
    }
     */
}

inline void ardubus_servo_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x53: // ASCII "S" (P<indexuint8_t><value>) //Note that the indexbyte is index of the servos-array, not pin number
            ardubus_servos[incoming_command[1]-ARDUBUS_INDEX_OFFSET].write(incoming_command[2]);
            Serial.print("S");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6, BYTE); // ACK
            break;
        case 0x73: // ASCII "s" (P<indexuint8_t><int_as_hex) //Note that the indexbyte is index of the servos-array, not pin number
            int value = ardubus_hex2int(incoming_command[2], incoming_command[3], incoming_command[4], incoming_command[5]);
            ardubus_servos[incoming_command[1]-ARDUBUS_INDEX_OFFSET].write(value);
            Serial.print("S");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.print(incoming_command[3]);
            Serial.print(incoming_command[4]);
            Serial.print(incoming_command[5]);
            Serial.println(0x6, BYTE); // ACK
            break;
    }
}

#endif
// *********** END OF CODE **********
