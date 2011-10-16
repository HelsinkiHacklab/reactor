/**
 * Test HW SPI for outputting to shift-register
 */
#include <SPI.h>


const byte resetpin = 10;
const byte oepin = 9;
const byte latchpin = 8;
const byte cnt_leds = 3*8;
byte reg_values[3];

void reset_regs()
{
    digitalWrite(resetpin, LOW);
    delayMicroseconds(5);
    digitalWrite(resetpin, HIGH);
}

void latch_clock()
{
    digitalWrite(latchpin, HIGH);
    delayMicroseconds(5);
    digitalWrite(latchpin, LOW);
}

void setup()
{
    Serial.begin(115200);
    SPI.begin();

    pinMode(10, OUTPUT); // Slave/Chip Select (we use this as ouput-enable)
    pinMode(11, OUTPUT); // MOSI
    pinMode(12, INPUT); // MISO (Do we need to have this as input or will the library choke if we use it for output ?)
    pinMode(13, OUTPUT); // Clock
    
    /*
    digitalWrite(10, LOW); // Slave/Chip Select (we use this as ouput-enable)
    digitalWrite(11, LOW); // MOSI
    digitalWrite(13, LOW); // Clock
    */


    pinMode(oepin, OUTPUT);
    digitalWrite(oepin, HIGH);
    pinMode(latchpin, OUTPUT);
    digitalWrite(HIGH, HIGH);
    pinMode(resetpin, OUTPUT);
    digitalWrite(resetpin, HIGH);

    SPI.setDataMode(SPI_MODE1);
    SPI.setBitOrder(LSBFIRST);
    SPI.setClockDivider(SPI_CLOCK_DIV4);

    digitalWrite(latchpin, LOW);
    reset_regs();
    digitalWrite(latchpin, HIGH);
    //clock_latch();
    analogWrite(oepin, 0xff-10);
    Serial.print("Booted");
}

void write_regs()
{
    reset_regs();
    digitalWrite(latchpin, LOW);
    for (byte i2=0; i2<sizeof(reg_values); i2++)
    {
        SPI.transfer(reg_values[i2]);
        //shiftOut(11, 13, MSBFIRST, reg_values[i2]);  
    }
    digitalWrite(latchpin, HIGH);
    // latch_clock();
}

void dump_regs()
{
        Serial.print("reg values");
        for (byte i2=0; i2<sizeof(reg_values); i2++)
        {
            Serial.print(" B");
            Serial.print(reg_values[i2], BIN);
        };
        Serial.println("");
}

/*
unsigned long timestamp;
unsigned long timestamp2;
*/
void loop()
{
    for (byte i=0; i<cnt_leds; i++)
    {
        // Calculate the bit in the correct register based on i, set it to 0 and others to 1
        byte reg = i/8;
        switch(reg) 
        {
            case 0:
              reg_values[0] = ~_BV((7-i%8));
              reg_values[1] = 0xff;
              reg_values[2] = 0xff;
              break;
            case 1:
              reg_values[0] = 0xff;
              reg_values[1] = ~_BV((7-i%8));
              reg_values[2] = 0xff;
              break;
            case 2:
              reg_values[1] = 0xff;
              reg_values[0] = 0xff;
              reg_values[2] = ~_BV((7-i%8));
              break;
        }
        Serial.print("Turning on LED ");
        Serial.println(i, DEC);
        write_regs();
        //dump_regs();
        delay(250);

        reg_values[reg] = 0xff;
        Serial.print("Turning off LED ");
        Serial.println(i, DEC);
        write_regs();
        delay(250);
    }
}
