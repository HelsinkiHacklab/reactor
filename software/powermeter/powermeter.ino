
/**
 * REMINDER: disconnect the current sensors from the board or uploading with ISP will get fsckd
 */
#define VCC_MV (5200) // I'm using 5.2V supply
#define MV_PER_LSB ((uint8_t)(VCC_MV/1024)) // I sure hope the complier will optimize these results to a constant
#define ACS715_ZERO ((uint16_t)(VCC_MV/10))
#define ACS714_ZERO ((uint16_t)(VCC_MV/2))

// Initialized the LCD library
#include <LiquidCrystalFast.h>
LiquidCrystalFast lcd(0, 1, 2, 7, 8, 9, 10); // LiquidCrystalFast lcd(RS, RW, Enable, D4, D5, D6, D7) 

// Convert the sensor reading from millivolts to milliamps
uint16_t acs715_mv2ma(uint16_t mv)
{
    // 133 mV/A starting at 500 mV (actually vcc/100), 1.5% error
    if (mv <= ACS715_ZERO)
    {
        return 0;
    }
    mv = mv - ACS715_ZERO; // Zero
    uint8_t amps = mv / 133;
    uint8_t desiamps = (mv - (amps*133)) / 13;
    uint8_t centiamps = (mv - (amps*133) - (desiamps*13));
    return (amps*1000) + (desiamps * 100) + (centiamps * 10);
}

// Get the sign of the corresponding reading
inline int8_t acs714_mv2ma_sign(uint16_t mv)
{
    if (mv < ACS714_ZERO)
    {
        return -1;
    }
    return 1;
}

// Convert the sensor reading from millivolts to milliamps
uint16_t acs714_mv2ma(uint16_t mv)
{
    // 66mV/A centered on 2500mv, 1.5% error
    // For now I'll just care about the positive side.
    if (mv <= ACS714_ZERO)
    {
        return 0;
    }
    mv = mv - ACS714_ZERO;
    uint8_t amps = mv / 66;
    uint8_t desiamps = (mv - (amps*66)) / 6;
    return (amps*1000) + (desiamps * 100);
}

// Converts a binary number (smaller than 10) to corresponding ASCII character
inline char num2ascii(uint8_t input)
{
    return input + 0x30;
}

// Formatter for the voltages an amperages, returns a char-pointer so can be called directly from lcd.print
char format_mx2x_buffer[5]; // space for "x.xx" and null)
char* format_mx2x(uint16_t mv)
{
    uint8_t x = mv / 1000;
    uint8_t cx = (mv - (x*1000)) / 100;
    // TODO: Due to the bug #58 this could be implemented inline and not including sprintf would probably save a lot of code size.
    //sprintf(format_mx2x_buffer, "%d.%02d", x, cx);
    format_mx2x_buffer[0] = num2ascii(x);
    format_mx2x_buffer[1] = 0x2e; // ASCII "."
    if (cx < 10)
    {
        format_mx2x_buffer[2] = 0x30; // ASCII "0";
        format_mx2x_buffer[3] = num2ascii(cx);
    }
    else
    {
        format_mx2x_buffer[2] = num2ascii(cx/10);
        format_mx2x_buffer[3] = num2ascii((cx-(format_mx2x_buffer[2]*10)));
    }
    format_mx2x_buffer[4] = 0x0;
    return format_mx2x_buffer;
}

// Variables for holding our sensor data, this set is already converted to mV based on the factors calculated earlier
uint16_t acs71x_3v3_mv; //3.3V side current sensor (A4)
uint16_t acs71x_5v_mv; // 5V side current sensor (A5)
uint16_t sense3v3_mv; // 3.3V side voltage monitor (A6)
uint16_t sense5v_mv; // 5V side voltage monitor (A7)

void setup()
{
    // set up the LCD's number of rows and columns: 
    lcd.begin(16, 2);
    //Print a boot message to the LCD.
    //lcd.print("Hello, world!");
    //delay(500);
    // And clear it
    lcd.clear();
}

void loop()
{
    // Read the sensors and apply mV factor
    acs71x_3v3_mv = analogRead(A4) * MV_PER_LSB;
    acs71x_5v_mv = analogRead(A5) * MV_PER_LSB;
    sense3v3_mv = analogRead(A6) * MV_PER_LSB;
    sense5v_mv = analogRead(A7) * MV_PER_LSB;

    // This will print the sensed data
    lcd.setCursor(0, 0);
    lcd.print(format_mx2x(sense5v_mv));
    lcd.print("V");
    lcd.setCursor(11, 0);
    lcd.print(format_mx2x(sense3v3_mv));
    lcd.print("V");
    lcd.setCursor(0, 1);
    lcd.print(format_mx2x(acs715_mv2ma(acs71x_5v_mv)));
    lcd.print("A");
    lcd.setCursor(11, 1);
    lcd.print(format_mx2x(acs714_mv2ma(acs71x_3v3_mv)));
    lcd.print("A");

    // We have 2*4 characters of space in the middle we could use if we can get around the codesize issue http://code.google.com/p/arduino-tiny/issues/detail?id=58

    delay(50);
}
