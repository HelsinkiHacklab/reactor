#ifndef ardubus_h
#define ardubus_h
#include <WProgram.h> 
#ifndef ARDUBUS_REPORT_INTERVAL
#define ARDUBUS_REPORT_INTERVAL 5000 // Milliseconds
#endif
#ifndef ARDUBUS_COMMAND_STRING_SIZE
#define ARDUBUS_COMMAND_STRING_SIZE 10 //Remember to allocate for the null termination
#endif
#ifndefARDUBUS_INDEX_OFFSET
#define ARDUBUS_INDEX_OFFSET 32 // We need to offset the pin/index numbers to above CR and LF which are control characters to us
#endif


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

// Handle incoming Serial data, try to find a command in there
char ardubus_incoming_command[ARDUBUS_COMMAND_STRING_SIZE+2]; //Reserve space for CRLF too.
byte ardubus_incoming_position;
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
            memset(&ardubus_incoming_command, 0, COMMAND_STRING_SIZE+2);
            ardubus_incoming_position = 0;
            return;
        }
        ardubus_incoming_position++;

        // Sanity check buffer sizes
        if (ardubus_incoming_position > COMMAND_STRING_SIZE+2)
        {
            Serial.println(0x15); // NACK
            Serial.print("PANIC: No end-of-line seen and ardubus_incoming_position=");
            Serial.print(ardubus_incoming_position, DEC);
            Serial.println(" clearing buffers");
            
            memset(&ardubus_incoming_command, 0, COMMAND_STRING_SIZE+2);
            ardubus_incoming_position = 0;
        }
    }
}

void ardubus_process_command()
{
#ifdef ARDUBUS_DIGITAL_INPUTS
    ardubus_digital_in_process_command();
#endif
#ifdef ARDUBUS_DIGITAL_OUTPUTS
    ardubus_digital_out_process_command();
#endif
#ifdef ARDUBUS_ANALOG_INPUTS
    ardubus_analog_in_process_command();
#endif
#ifdef ARDUBUS_PWM_OUTPUTS
    ardubus_pwm_out_process_command();
#endif
#ifdef ARDUBUS_SERVO_OUTPUTS
    ardubus_servo_process_command();
#endif
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
    ardubus_check_report();
}


#endif
// *********** END OF CODE **********
