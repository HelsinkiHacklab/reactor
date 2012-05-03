/**
 * Use the RGB (3x PCA9625 drivers in a handy configuration) led driver board as "Just a Bunch Of LEDs"
 * 
 * @see https://github.com/HelsinkiHacklab/reactor/blob/master/blueprints/ledcontroller.brd
 *
 * Remember your I2C pull-up resistors
 */
// Get this from http://dsscircuits.com/articles/arduino-i2c-master-library.html
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
// For the weirdest reason this does not get to the scope of the libraries
#define I2C_DEVICE_DEBUG
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGB.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGBJBOL.h>
#include <Bounce.h>

#define SWITCHPIN A0

// Container for the device
pca9635RGBJBOL driverboard;


Bounce bouncer = Bounce(SWITCHPIN, 250); 

void setup()
{
    Serial.begin(115200);
    
    pinMode(SWITCHPIN, INPUT);          
    digitalWrite(SWITCHPIN, HIGH); // pull-up
    
    
    I2c.begin();
    I2c.timeOut(500); // 500ms timeout to avoid lockups
    I2c.pullup(false); //Disable internal pull-ups
    I2c.setSpeed(true); // Fast-mode support

    // Set device address and call I2c.begin()
    Serial.println("Initializing led drivers");
    driverboard.begin(0);

    // Dump the driver mode registers to check they're correct
    driverboard.R.dump_registers(0x0, 0x01);
    driverboard.G.dump_registers(0x0, 0x01);
    driverboard.B.dump_registers(0x0, 0x01);
    // Dump the led mode registers to check they're correct
    driverboard.R.dump_registers(0x14, 0x17);
    driverboard.G.dump_registers(0x14, 0x17);
    driverboard.B.dump_registers(0x14, 0x17);



    Serial.println("Booted");
}

const byte test_leds_max = 16*3;
byte ledno=255;
byte bstate;
void loop()
{
    if (bouncer.update())
    {
        bstate = bouncer.read();
        Serial.print("State ");
        Serial.println(bstate, DEC);
        if (bstate)
        {
            Serial.print("Turning OFF led ");
            Serial.println(ledno, DEC);
            driverboard.set_led_pwm(ledno, 0);
    
            ledno++;
            ledno = ledno % test_leds_max;
    
            Serial.print("Turning ON led ");
            Serial.println(ledno, DEC);
            driverboard.set_led_pwm(ledno, 255);
            
        }
    }
    
    /*
    for (byte ledno = 0; ledno < test_leds_max; ledno++)
    {
        Serial.print("Turning on led ");
        Serial.println(ledno, DEC);
        //driverboard.set_led_mode(ledno, 1);
        driverboard.set_led_pwm(ledno, 255);
        delay(250);
        Serial.print("Turning off led ");
        Serial.println(ledno, DEC);
        driverboard.set_led_pwm(ledno, 0);
        //driverboard.set_led_mode(ledno, 0);
    }
    */
}
