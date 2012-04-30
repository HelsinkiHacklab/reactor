#ifndef ardubus_h
#define ardubus_h
#include <Arduino.h> 
#ifndef ARDUBUS_REPORT_INTERVAL
#define ARDUBUS_REPORT_INTERVAL 5000 // Milliseconds
#endif
#ifndef ARDUBUS_COMMAND_STRING_SIZE
#define ARDUBUS_COMMAND_STRING_SIZE 8 //Remember to allocate for the null termination
#endif
#ifndef ARDUBUS_INDEX_OFFSET
#define ARDUBUS_INDEX_OFFSET 32 // We need to offset the pin/index numbers to above CR and LF which are control characters to us
#endif

/**
 * Parses ASCII [0-9A-F] hexadecimal to byte value
 */
inline byte ardubus_hex2byte(byte hexchar)
{
    if (   0x40 < hexchar
        && hexchar < 0x47) // A-F
    {
        return (hexchar - 0x41) + 10; 
    }
    if (   0x2f < hexchar
        && hexchar < 0x3a) // 0-9
    {
        return (hexchar - 0x30);
    }
    return 0x0; // Failure.
    
}

inline byte ardubus_hex2byte(byte hexchar0, byte hexchar1)
{
    return (ardubus_hex2byte(hexchar0) << 4) | ardubus_hex2byte(hexchar1);
}

inline int ardubus_hex2int(byte hexchar0, byte hexchar1, byte hexchar2, byte hexchar3)
{
    return ardubus_hex2byte(hexchar0, hexchar1) << 8 | ardubus_hex2byte(hexchar2, hexchar3);
}

/**
 * The new arduino does not support the BYTE keyword and in any case this allows for easier change of the ACK sequence
 */
inline void ardubus_ack()
{
    Serial.write(0x6);
    Serial.println("");
}

// Utility functions for outputting fixed lenght nex encoded numbers
inline void ardubus_print_byte_as_2hex(byte input)
{
    if (input < 0x10)
    {
        Serial.print("0");
    }
    Serial.print(input, HEX);
}

inline void ardubus_print_ulong_as_8hex(unsigned long input)
{
    ardubus_print_byte_as_2hex((byte)(input >> 24));
    ardubus_print_byte_as_2hex((byte)((input >> 16) & 0xff));
    ardubus_print_byte_as_2hex((byte)((input >> 8) & 0xff));
    ardubus_print_byte_as_2hex((byte)(input & 0xff));
}

inline void ardubus_print_int_as_4hex(int input)
{
    ardubus_print_byte_as_2hex((byte)(input >> 8));
    ardubus_print_byte_as_2hex((byte)(input & 0xff));
}

// Include enabled submodules
#ifdef ARDUBUS_DIGITAL_INPUTS
#include "ardubus_digital_in.h"
#endif
#ifdef ARDUBUS_DIGITAL_OUTPUTS
#include "ardubus_digital_out.h"
#endif
#ifdef ARDUBUS_ANALOG_INPUTS
#include "ardubus_analog_in.h"
#endif
#ifdef ARDUBUS_PWM_OUTPUTS
#include "ardubus_pwm_out.h"
#endif
#ifdef ARDUBUS_SERVO_OUTPUTS
#include "ardubus_servo.h"
#endif
#ifdef ARDUBUS_PCA9635RGBJBOL_BOARDS
#include "ardubus_pca9635RGBJBOL.h"
#endif
#ifdef ARDUBUS_SPI74XX595_REGISTER_COUNT
#include "ardubus_spi74XX595.h"
#endif
#ifdef ARDUBUS_PCA9535_INPUTS
#include "ardubus_pca9535_in.h"
#endif


/**
 * Setups up all enabled submodules
 */
void ardubus_setup()
{
#ifdef ARDUBUS_DIGITAL_INPUTS
    ardubus_digital_in_setup();
#endif
#ifdef ARDUBUS_DIGITAL_OUTPUTS
    ardubus_digital_out_setup();
#endif
#ifdef ARDUBUS_ANALOG_INPUTS
    ardubus_analog_in_setup();
#endif
#ifdef ARDUBUS_PWM_OUTPUTS
    ardubus_pwm_out_setup();
#endif
#ifdef ARDUBUS_SERVO_OUTPUTS
    ardubus_servo_setup();
#endif
#ifdef ARDUBUS_PCA9635RGBJBOL_BOARDS
    ardubus_pca9635RGBJBOL_setup();
#endif
#ifdef ARDUBUS_SPI74XX595_REGISTER_COUNT
    ardubus_spi74XX595_setup();
#endif
#ifdef ARDUBUS_PCA9535_INPUTS
    ardubus_pca9535_in_setup();
#endif
}


// Call the report function on all supported submodules
unsigned long ardubus_last_report_time;
void ardubus_report()
{
#ifdef ARDUBUS_DIGITAL_INPUTS
    ardubus_digital_in_report();
#endif
#ifdef ARDUBUS_DIGITAL_OUTPUTS
    ardubus_digital_out_report();
#endif
#ifdef ARDUBUS_ANALOG_INPUTS
    ardubus_analog_in_report();
#endif
#ifdef ARDUBUS_PWM_OUTPUTS
    ardubus_pwm_out_report();
#endif
#ifdef ARDUBUS_SERVO_OUTPUTS
    ardubus_servo_report();
#endif
#ifdef ARDUBUS_PCA9635RGBJBOL_BOARDS
    ardubus_pca9635RGBJBOL_report();
#endif
#ifdef ARDUBUS_SPI74XX595_REGISTER_COUNT
    ardubus_spi74XX595_report();
#endif
#ifdef ARDUBUS_PCA9535_INPUTS
    ardubus_pca9535_in_report();
#endif
    ardubus_last_report_time = millis();
}

// Check if we should send the report (called in ardubus_update)
inline void ardubus_check_report()
{
    if ((millis() - ardubus_last_report_time) > ARDUBUS_REPORT_INTERVAL)
    {
        ardubus_report();
    }
}


// We need to declare this early
char ardubus_incoming_command[ARDUBUS_COMMAND_STRING_SIZE+2]; //Reserve space for CRLF too.
byte ardubus_incoming_position;
void ardubus_process_command()
{
#ifdef ARDUBUS_DIGITAL_INPUTS
    ardubus_digital_in_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_DIGITAL_OUTPUTS
    ardubus_digital_out_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_ANALOG_INPUTS
    ardubus_analog_in_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_PWM_OUTPUTS
    ardubus_pwm_out_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_SERVO_OUTPUTS
    ardubus_servo_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_PCA9635RGBJBOL_BOARDS
    ardubus_pca9635RGBJBOL_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_SPI74XX595_REGISTER_COUNT
    ardubus_spi74XX595_process_command(ardubus_incoming_command);
#endif
#ifdef ARDUBUS_PCA9535_INPUTS
    ardubus_pca9535_in_process_command(ardubus_incoming_command);
#endif
}

// Handle incoming Serial data, try to find a command in there
inline void ardubus_read_command_bytes()
{
    for (byte d = Serial.available(); d > 0; d--)
    {
        ardubus_incoming_command[ardubus_incoming_position] = Serial.read();
        // Check for line end and in such case do special things
        if (   ardubus_incoming_command[ardubus_incoming_position] == 0xA // LF
            || ardubus_incoming_command[ardubus_incoming_position] == 0xD) // CR
        {
            ardubus_incoming_command[ardubus_incoming_position] = 0x0;
            if (   ardubus_incoming_position > 0
                && (   ardubus_incoming_command[ardubus_incoming_position-1] == 0xD // CR
                    || ardubus_incoming_command[ardubus_incoming_position-1] == 0xA) // LF
               )
            {
                ardubus_incoming_command[ardubus_incoming_position-1] = 0x0;
            }
            ardubus_process_command();
            // Clear the buffer and reset position to 0
            memset(&ardubus_incoming_command, 0, ARDUBUS_COMMAND_STRING_SIZE+2);
            ardubus_incoming_position = 0;
            return;
        }
        ardubus_incoming_position++;

        // Sanity check buffer sizes
        if (ardubus_incoming_position > ARDUBUS_COMMAND_STRING_SIZE+2)
        {
            Serial.println(0x15); // NACK
            Serial.print("PANIC: No end-of-line seen and ardubus_incoming_position=");
            Serial.print(ardubus_incoming_position, DEC);
            Serial.println(" clearing buffers");
            
            memset(&ardubus_incoming_command, 0, ARDUBUS_COMMAND_STRING_SIZE+2);
            ardubus_incoming_position = 0;
        }
    }
}

/**
 * called in mainloop at each iteration, calls corresponding functions on all enabled submodules
 */
void ardubus_update()
{
    ardubus_read_command_bytes();
#ifdef ARDUBUS_DIGITAL_INPUTS
    ardubus_digital_in_update();
#endif
#ifdef ARDUBUS_DIGITAL_OUTPUTS
    ardubus_digital_out_update();
#endif
#ifdef ARDUBUS_ANALOG_INPUTS
    ardubus_analog_in_update();
#endif
#ifdef ARDUBUS_PWM_OUTPUTS
    ardubus_pwm_out_update();
#endif
#ifdef ARDUBUS_SERVO_OUTPUTS
    ardubus_servo_update();
#endif
#ifdef ARDUBUS_PCA9635RGBJBOL_BOARDS
    ardubus_pca9635RGBJBOL_update();
#endif
#ifdef ARDUBUS_SPI74XX595_REGISTER_COUNT
    ardubus_spi74XX595_update();
#endif
#ifdef ARDUBUS_PCA9535_INPUTS
    ardubus_pca9535_in_update();
#endif
    ardubus_check_report();
}


#endif
// *********** END OF CODE **********
