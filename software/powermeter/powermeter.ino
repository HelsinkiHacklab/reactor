
/**
 * REMINDER: disconnect the current sensors from the board or uploading with ISP will get fsckd
 *
 * NOTE: You must replace your Arduino linker, see  http://code.google.com/p/arduino-tiny/issues/detail?id=58
 *
 */
#define VCC_MV (5200) // I'm using 5.2V supply
#define ACS715_ZERO ((uint16_t)(VCC_MV/10))
#define ACS714_ZERO ((uint16_t)(VCC_MV/2))

const float MV_PER_LSB = (float)VCC_MV/1024.0;


// Initialized the LCD library
#include <LiquidCrystalFast.h>
LiquidCrystalFast lcd(0, 1, 2, 7, 8, 9, 10); // LiquidCrystalFast lcd(RS, RW, Enable, D4, D5, D6, D7) 

// Convert the sensor reading from millivolts to milliamps
uint16_t acs715_mv2ma2(uint16_t mv)
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

uint16_t acs715_mv2ma(float mv)
{
    // 133 mV/A starting at 500 mV (actually vcc/100), 1.5% error
    if (mv <= ACS715_ZERO)
    {
        return 0;
    }
    mv = mv - ACS715_ZERO; // Zero
    float amps = mv / 133.0;
    return (uint16_t)(amps*1000);
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
uint16_t acs714_mv2ma2(uint16_t mv)
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

uint16_t acs714_mv2ma(float mv)
{
    // 66mV/A centered on 2500mv, 1.5% error
    // For now I'll just care about the positive side.
    if (mv <= ACS714_ZERO)
    {
        return 0;
    }
    mv = mv - ACS714_ZERO;
    float amps = mv / 66;
    return (uint16_t)(amps*1000);
}


// Formatter for the voltages an amperages, returns a char-pointer so can be called directly from lcd.print
char format_mx2x_buffer[6]; // space for "x.xx" and null)
char* format_mx2x(uint16_t mv)
{
    uint8_t x = mv / 1000;
    uint8_t cx = (mv % 1000) / 10;
    sprintf(format_mx2x_buffer, "%02d.%02d", x, cx);
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
    lcd.print(F("Hello, world!"));
    delay(500);
    // And clear it
    lcd.clear();
}

void loop()
{
    /*
    // Read the sensors and apply mV factor
    acs71x_3v3_mv = analogRead(A4) * MV_PER_LSB;
    acs71x_5v_mv = analogRead(A5) * MV_PER_LSB;
    sense3v3_mv = analogRead(A6) * MV_PER_LSB;
    sense5v_mv = analogRead(A7) * MV_PER_LSB;

    // This will print the sensed data
    lcd.setCursor(0, 0);
    lcd.print(format_mx2x(sense5v_mv));
    lcd.print("V");
    lcd.setCursor(10, 0);
    lcd.print(format_mx2x(sense3v3_mv));
    lcd.print("V");
    lcd.setCursor(0, 1);
    lcd.print(format_mx2x(acs715_mv2ma(acs71x_5v_mv)));
    lcd.print("A");
    lcd.setCursor(10, 1);
    lcd.print(format_mx2x(acs714_mv2ma(acs71x_3v3_mv)));
    lcd.print("A");
    */

    // Print just the analogRead data
    lcd.setCursor(0, 0);
    sprintf(format_mx2x_buffer, "%04d", analogRead(A7));
    lcd.print(format_mx2x_buffer);
    lcd.setCursor(10, 0);
    sprintf(format_mx2x_buffer, "%04d", analogRead(A6));
    lcd.print(format_mx2x_buffer);
    lcd.setCursor(0, 1);
    sprintf(format_mx2x_buffer, "%04d", analogRead(A5));
    lcd.print(format_mx2x_buffer);
    lcd.setCursor(10, 1);
    sprintf(format_mx2x_buffer, "%04d", analogRead(A4));
    lcd.print(format_mx2x_buffer);

    // We have 2*2 characters of space in the middle we could use (or 2*4 if we're carefull not to make the main point unreadable)

    delay(250);
}
