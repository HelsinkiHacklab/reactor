#include <Bounce.h>
#include <MsTimer2.h>
#include <Servo.h>
#define PIN_OFFSET 32 // We need to offset the pin numbers to above CR and LF which are control characters to us
/**
 * Notes about ports on Seeduino Mega
 *
 * PORTA Pins 22-29
 * PORTB 53,52-50(SPI),10-13 (NOTE: pin13 has the led and it has resistor, thus the internal pull-up can't be used with it)
 * PORTC Pins 30-37
 * <PORTD 3-4(I2C),RX1-RX2,PD4-PD6,38>
 * <PORTE can't be used, had RX0/TX0 which we need.>
 * PORTF Analog normal 0-7
 * PORTG 39-41,4,PG4-PG3, (NOTE PG6-7 are missing)
 * PORTH RX2-TX2,PH2,6-9,PH7
 * PORTK Analog mega 8-15
 * PORTL Pins 42-49
 *
 * See timers http://softsolder.com/2010/09/05/arduino-mega-1280-pwm-to-timer-assignment/
 */

// Define the input pins we wish to use
const byte d_input_pins[] = { 2, 24, 32, 50, PJ6, 44 }; // Digital inputs, debounced
const byte a_input_pins[] = { A1 }; // Analog inputs, unfiltered
#define ANALOG_READ_INTERVAL 5 // Milliseconds
// Define output pins we wish to use
const byte d_output_pins[] = { 13 }; // Digital outputs, including HW PMW (you are responsible for only calling the HW PWM for pins that actually support it)
const byte s_output_pins[] = { 10 }; // Servo outputs

#define DEBOUNCE_TIME 20 // milliseconds, see Bounce library
#define DEBOUNCE_UPDATE_TIME 5 // Milliseconds, how often to call update() on the debouncers, see Bounce library
#define REPORT_INTERVAL 5000 // Milliseconds




// Initialize the array of debouncers and servos
Bounce bouncers[sizeof(d_input_pins)] = Bounce(d_input_pins[0],DEBOUNCE_TIME); // We must initialize these here or things break, will overwrite with new instances in setup()
Servo servos[sizeof(s_output_pins)] = Servo();

inline void setup_a_inputs()
{
    for (byte i=0; i < sizeof(a_input_pins); i++)
    {
        pinMode(a_input_pins[i], INPUT);
        digitalWrite(a_input_pins[i], LOW); // Make sure the internal pull-up is disabled
    }
}

// Initialize the servos
inline void setup_s_outputs()
{
    for (byte i=0; i < sizeof(s_output_pins); i++)
    {
        servos[i].attach(s_output_pins[i]);
        servos[i].write(90);
    }
}

// Initialize digital output pins
inline void setup_d_outputs()
{
    for (byte i=0; i < sizeof(d_output_pins); i++)
    {
        pinMode(d_output_pins[i], OUTPUT);
        digitalWrite(d_output_pins[i], LOW);
    }
}

// Initialize the digital input pins and their debouncers
inline void setup_bouncer()
{
    // Setup the debouncers
    for (byte i=0; i < sizeof(d_input_pins); i++)
    {
        pinMode(d_input_pins[i], INPUT);
        if (d_input_pins[i] != 13)
        {
            digitalWrite(d_input_pins[i], HIGH); // enable internal pull-up (except for #13 which has the led and external resistor, which will cause issues, see http://www.arduino.cc/en/Tutorial/DigitalPins)
        }
        bouncers[i] = Bounce(d_input_pins[i], DEBOUNCE_TIME);
    }
}


void setup()
{
    Serial.begin(115200);
    
    setup_d_outputs();
    setup_bouncer();
    Serial.println("Booted");
}

// Report input pin states via Serial
unsigned long last_report_time;
void report()
{
    for (byte i=0; i < sizeof(d_input_pins); i++)
    {
        Serial.print("RD"); // RD<pin_byte><state_byte><time_long_as_hex>
        Serial.print(d_input_pins[i]);
        Serial.print(bouncers[i].read());
        // This might not be the best way to pass this info, maybe fixed-lenght encoding would be better ?
        Serial.println(bouncers[i].duration(), HEX);
    }
    last_report_time = millis();
}

// Check if we should send the report (called in mainloop)
inline void check_report()
{
    if ((millis() - last_report_time) > REPORT_INTERVAL)
    {
        report();
    }
}

// Check if we should debounce (called in mainloop)
unsigned long last_debounce_time;
inline void check_debounce()
{
    if ((millis() - last_debounce_time) > DEBOUNCE_UPDATE_TIME)
    {
        update_bouncers();
    }
}

// Calls update method on all of the digital inputs and outputs message to Serial if state changed
inline void update_bouncers()
{
    // Update debouncer states
    for (byte i=0; i < sizeof(d_input_pins); i++)
    {
        if (bouncers[i].update())
        {
            // State changed
            Serial.print("CD"); // CD<pin_byte><state_byte>
            Serial.print(d_input_pins[i]);
            Serial.println(bouncers[i].read());
        }
    }
    last_debounce_time = millis();
}


// Check if we should debounce (called in mainloop)
unsigned long last_aread_time;
inline void check_aread()
{
    if ((millis() - last_aread_time) > ANALOG_READ_INTERVAL)
    {
        update_analog_inputs();
    }
}

inline void update_analog_inputs()
{
    for (byte i=0; i < sizeof(a_input_pins); i++)
    {
        Serial.print("CA"); // CA<pin_byte><value in hex>
        Serial.print(a_input_pins[i]);
        // This might not be the best way to pass this info, maybe fixed-lenght encoding would be better ?
        Serial.println(analogRead(a_input_pins[i]), HEX);
    }
    last_aread_time = millis();
}


// Handle incoming Serial data, try to find a command in there
#define COMMAND_STRING_SIZE 10 //Remember to allocate for the null termination
char incoming_command[COMMAND_STRING_SIZE+2]; //Reserve space for CRLF too.
byte incoming_position;
inline void read_command_bytes()
{
    for (byte d = Serial.available(); d > 0; d--)
    {
        incoming_command[incoming_position] = Serial.read();
        // Check for line end and in such case do special things
        if (   incoming_command[incoming_position] == 0xA // LF
            || incoming_command[incoming_position] == 0xD) // CR
        {
            incoming_command[incoming_position] = 0x0;
            if (   incoming_position > 0
                && (   incoming_command[incoming_position-1] == 0xD // CR
                    || incoming_command[incoming_position-1] == 0xA) // LF
               )
            {
                incoming_command[incoming_position-1] = 0x0;
            }
            process_command();
            incoming_position = 0;
            return;
        }
        incoming_position++;

        // Sanity check buffer sizes
        if (incoming_position > COMMAND_STRING_SIZE+2)
        {
            Serial.println(0x15); // NACK
            Serial.print("PANIC: No end-of-line seen and incoming_position=");
            Serial.print(incoming_position, DEC);
            Serial.println(" clearing buffers");
            
            memset(&incoming_command, 0, COMMAND_STRING_SIZE+2);
            incoming_position = 0;
        }
    }
}


/**
 * Helper to combine two bytes as int
 */
inline int bytes2int(byte i1, byte i2)
{
    int tmp = i1;
    tmp <<= 8;
    tmp += i2;
    return tmp;
}

// Parse the command received
void process_command()
{
    switch(incoming_command[0])
    {
        case 0x44: // ASCII "D" (D<pinbyte><statebyte>) //The pin must have been declared in d_output_pins or unexpected things will happen
            if (incoming_command[2] == 0x31) // ASCII "1"
            {
                digitalWrite(incoming_command[1]-PIN_OFFSET, HIGH);
            }
            else
            {
                digitalWrite(incoming_command[1]-PIN_OFFSET, LOW);
            }
            Serial.print("D");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6); // ACK
            break;
        case 0x50: // ASCII "P" (P<pinbyte><cyclebyte>) //The pin must have been declared in d_output_pins or unexpected things will happen (and must support HW PWM)
            analogWrite(incoming_command[1]-PIN_OFFSET, incoming_command[2]);
            Serial.print("P");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6); // ACK
            break;
        case 0x53: // ASCII "S" (P<indexbyte><value>) //Note that the indexbyte is index of the servos-array, not pin number
            servos[incoming_command[1]].write(incoming_command[2]);
            Serial.print("S");
            Serial.print(incoming_command[1]);
            Serial.print(incoming_command[2]);
            Serial.println(0x6); // ACK
            break;
        default:
            Serial.println(0x15); // NACK
            return;
            break;
    }
}


void loop()
{
    check_debounce();
    check_aread();
    check_report();
    read_command_bytes();
}
