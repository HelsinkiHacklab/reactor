#include <Bounce.h>
#include <MsTimer2.h>

/**
 * Notes about ports on Seeduino Mega
 *
 * PORTA Pins 22-29
 * PORTB 53,52-50(SPI),10-13
 * PORTC Pins 30-37
 * <PORTD 3-4(I2C),RX1-RX2,PD4-PD6,38>
 * <PORTE can't be used, had RX0/TX0 which we need.>
 * PORTF Analog normal 0-7
 * PORTG 39-41,4,PG4-PG3, (NOTE PG6-7 are missing)
 * PORTH RX2-TX2,PH2,6-9,PH7
 * PORTK Analog mega 8-15
 * PORTL Pins 42-49
 */

// Define the input pins we wish to use
const byte inputpins[] = { 2, 24, 32, 50, PJ6, 44 };
#define DEBOUNCE_TIME 20 // milliseconds, see Bounce library
#define REPORT_INTERVAL 5000 // Milliseconds




// Initialize the array of debouncers
Bounce bouncers[sizeof(inputpins)] = Bounce(inputpins[0],DEBOUNCE_TIME); // We must initialize these or things break

boolean update_bouncers_flag;
void flag_update_bouncer()
{
    update_bouncers_flag = true;
}

inline void setup_bouncer()
{
    // Setup the debouncers
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        pinMode(inputpins[i], INPUT);
        digitalWrite(inputpins[i], HIGH); // enable internal pull-up
        bouncers[i] = Bounce(inputpins[i], DEBOUNCE_TIME);
    }
}

inline void update_bouncers()
{
    // Update debouncer states
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        if (bouncers[i].update())
        {
            // State changed
            /*
            Serial.print("Pin ");
            Serial.print(inputpins[i], DEC);
            Serial.print(" CHANGED to ");
            Serial.println(bouncers[i].read(), DEC);
            */
            Serial.print("CD"); // CD<pin_byte><state_byte>
            Serial.print(inputpins[i]);
            Serial.println(bouncers[i].read());
        }
    }
    update_bouncers_flag = false;
}

void setup()
{
    Serial.begin(115200);
    
    setup_bouncer();
    // Setup timer for flagging bouncer updates
    MsTimer2::set(5, flag_update_bouncer);
    MsTimer2::start();

    Serial.println("Booted");
}

unsigned long last_report_time;
void report()
{
    for (byte i=0; i < sizeof(inputpins); i++)
    {
        /*
        Serial.print("Pin ");
        Serial.print(inputpins[i], DEC);
        Serial.print(" state has been ");
        Serial.print(bouncers[i].read(), DEC);
        Serial.print(" for ");
        Serial.print(bouncers[i].duration(), DEC);
        Serial.println("ms");
        */
        Serial.print("RD"); // RD<pin_byte><state_byte><time_long_as_hex>
        Serial.print(inputpins[i]);
        Serial.print(bouncers[i].read());
        Serial.println(bouncers[i].duration(), HEX);
    }
    last_report_time = millis();
}

inline void check_report()
{
    if ((millis() - last_report_time) > REPORT_INTERVAL)
    {
        report();
    }
}

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

void process_command()
{
    switch(incoming_command[0])
    {
        case 0x0:
            Serial.println(0x15); // NACK
            return;
            break;
        case 0x44: // ASCII "D" (D<pinbyte><statebyte>)
            if (incoming_command[2])
            {
                digitalWrite(incoming_command[1], HIGH);
            }
            else
            {
                digitalWrite(incoming_command[1], LOW);
            }
            Serial.println(0x6); // ACK
            break;
    }
}


void loop()
{
    if (update_bouncers_flag)
    {
        update_bouncers();
    }
    check_report();
}
