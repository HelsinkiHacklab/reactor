#ifndef ardubus_servo_h
#define ardubus_servo_h
#include <WProgram.h> 
#include <Servo.h>

// Enumerate the servo pins from the preprocessor
const byte ardubus_servo_output_pins[] = ARDUBUS_SERVO_OUTPUTS;
// Declare a Servo object for each
Servo ardubus_servos[sizeof(ardubus_servo_output_pins)] = Servo();

inline void ardubus_servo_setup()
{
    for (byte i=0; i < sizeof(ardubus_servo_output_pins); i++)
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
    for (byte i=0; i < sizeof(ardubus_servo_output_pins); i++)
    {
        Serial.print("RS"); // RS<index_byte><value in hex>
        Serial.print(i);
        // This might not be the best way to pass this info, maybe fixed-lenght encoding would be better ?
        Serial.println(ardubus_servos[i].read(), HEX);
        // TODO: Keep track of duration ??
    }
}

inline void ardubus_servo_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x53: // ASCII "S" (P<indexbyte><value>) //Note that the indexbyte is index of the servos-array, not pin number
            ardubus_servos[incoming_command[1]-ARDUBUS_INDEX_OFFSET].write(incoming_command[2]);
            Serial.print("S");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6); // ACK
            break;
    }
}

#endif
// *********** END OF CODE **********
