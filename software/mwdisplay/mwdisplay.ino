/**
 * I2C to 7-segment adapter for ATTiny85
 */

/*
// hello
[ 8 0 68 65 6c 6c 6f ]

// 0-4
[ 8 0 30 31 32 33 34 ]
// 5-9
[ 8 0 35 36 37 38 39 ]

// 1- 3
[ 8 0 31 32 33 ]

// a - e
[ 8 0 61 62 63 64 65 ]
// f - h
[ 8 0 66 67 68 69 6a ]
// o-
[ 8 0 6f 70 71 72 73 ]


// A - E
[ 8 0 41 42 43 44 45 ]
// F-H
[ 8 0 46 47 48 49 4a ]
// O-
[ 8 0 4f 50 51 52 53 ]

// HELLO
[ 8 0 48 45 4c 4c 4f ]

// Read the registers
[ 8 0 ] [ 9 r r r r r ]

*/


/**
 * Pin notes by Suovula, see also http://hlt.media.mit.edu/?p=1229
 *
 * DIP and SOIC have same pinout, however the SOIC chips are much cheaper, especially if you buy more than 5 at a time
 * For nice breakout boards see https://github.com/rambo/attiny_boards
 *
 * Basically the arduino pin numbers map directly to the PORTB bit numbers.
 *
// I2C
arduino pin 0 = not(OC1A) = PORTB <- _BV(0) = SOIC pin 5 (I2C SDA, PWM)
arduino pin 2 =           = PORTB <- _BV(2) = SOIC pin 7 (I2C SCL, Analog 1)
// Timer1 -> PWM
arduino pin 1 =     OC1A  = PORTB <- _BV(1) = SOIC pin 6 (PWM)
arduino pin 3 = not(OC1B) = PORTB <- _BV(3) = SOIC pin 2 (Analog 3)
arduino pin 4 =     OC1B  = PORTB <- _BV(4) = SOIC pin 3 (Analog 2)
 */
#define I2C_SLAVE_ADDRESS 0x4 // the 7-bit address (remember to change this when adapting this example)
// Get this from https://github.com/rambo/TinyWire
#include <TinyWireS.h>
// The default buffer size, Can't recall the scope of defines right now
#ifndef TWI_RX_BUFFER_SIZE
#define TWI_RX_BUFFER_SIZE ( 16 )
#endif
// We need to include pgmspace here too
#include "asciitable.h"
#define __PROG_TYPES_COMPAT__ 
#include <avr/pgmspace.h>

#define NUMBERS_COUNT 5
#define DATAPIN 1
#define CLOCKPIN 4
#define LATCHPIN 3

volatile uint8_t i2c_regs[NUMBERS_COUNT];
// Tracks the current register pointer position
volatile byte reg_position;
// See if we need to shift out data
volatile boolean start_shift;

// Store a hello-message in progrem
const char hello_str[] PROGMEM =  { 0x48, 0x45, 0x4c, 0x4c, 0x4f };


/**
 * This is called for each read request we receive, never put more than one byte of data (with TinyWireS.send) to the 
 * send-buffer when using this callback
 */
void requestEvent()
{  
    TinyWireS.send(i2c_regs[reg_position]);
    // Increment the reg position on each read, and loop back to zero
    reg_position = (reg_position+1) % sizeof(i2c_regs);
}


/**
 * The I2C data received -handler
 *
 * This needs to complete before the next incoming transaction (start, data, restart/stop) on the bus does
 * so be quick, set flags for long running tasks to be called from the mainloop instead of running them directly,
 */
void receiveEvent(uint8_t howMany)
{
    if (howMany < 1)
    {
        // Sanity-check
        return;
    }
    if (howMany > TWI_RX_BUFFER_SIZE)
    {
        // Also insane number
        return;
    }

    reg_position = TinyWireS.receive();
    howMany--;
    if (!howMany)
    {
        // This write was only to set the buffer for next read
        return;
    }
    while(howMany--)
    {
        i2c_regs[reg_position%sizeof(i2c_regs)] = TinyWireS.receive();
        reg_position++;
    }
    // Clear rest of the registers
    for (byte clearer = reg_position; clearer < sizeof(i2c_regs); clearer++)
    {
        i2c_regs[clearer] = 0x0;
    }
    start_shift = true;
}


void setup()
{
    pinMode(DATAPIN, OUTPUT);
    pinMode(CLOCKPIN, OUTPUT);
    pinMode(LATCHPIN, OUTPUT);
    digitalWrite(LATCHPIN, HIGH);
    delay(100);

    // Copy a string from program memory and display for a second
    for (byte i=0; i < sizeof(hello_str); i++)
    {
        i2c_regs[i] = pgm_read_byte_near(hello_str+i);
    }
    shift_registers();
    delay(1000);
    blank();

    /**
     * Reminder: taking care of pull-ups is the masters job
     */
    TinyWireS.begin(I2C_SLAVE_ADDRESS);
    TinyWireS.onReceive(receiveEvent);
    TinyWireS.onRequest(requestEvent);

}

/**
 * Blanks the screen but does not touch ic2_registers
 */
inline void blank()
{
    digitalWrite(LATCHPIN, LOW);
    for (byte i=0; i < NUMBERS_COUNT; i++)
    {
        shiftOut(DATAPIN, CLOCKPIN, MSBFIRST, 0xff);
    }
    digitalWrite(LATCHPIN, HIGH);
}

/**
 * Shifts out the data in i2c_registers, translating the ASCII codes to bit patterns
 * according the font in asciitable.h
 */
inline void shift_registers()
{
    digitalWrite(LATCHPIN, LOW);
    /**
     * For checking bit-patterns
    for (byte i=0; i < sizeof(i2c_regs); i++)
    {
        shiftOut(DATAPIN, CLOCKPIN, MSBFIRST, i2c_regs[i]);
    }
    */
    byte skipped = 0;
    // For normal output output in reverse order
    for (byte d=sizeof(i2c_regs); d > 0; d--)
    {
        // Skip null values (and increment counter used to clear the remaining digits)
        if (i2c_regs[d-1] == 0x0)
        {
            skipped++;
            continue;
        }
        shiftOut(DATAPIN, CLOCKPIN, MSBFIRST, ascii_to_7seg(i2c_regs[d-1]));
    }
    // Pad with empty
    while(skipped--)
    {
        shiftOut(DATAPIN, CLOCKPIN, MSBFIRST, 0xff);
    }
    digitalWrite(LATCHPIN, HIGH);
}

void loop()
{
    /**
     * This is the only way we can detect stop condition (http://www.avrfreaks.net/index.php?name=PNphpBB2&file=viewtopic&p=984716&sid=82e9dc7299a8243b86cf7969dd41b5b5#984716)
     * it needs to be called in a very tight loop in order not to miss any (REMINDER: Do *not* use delay() anywhere, use tws_delay() instead).
     * It will call the function registered via TinyWireS.onReceive(); if there is data in the buffer on stop.
     */
    TinyWireS_stop_check();
    if (start_shift)
    {
        start_shift = false;
        shift_registers();
    }
}
