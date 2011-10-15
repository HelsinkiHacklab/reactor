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
 
#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_DIGITAL_INPUTS { 2, 24, 32, 50, 44, PJ6, PJ7 }
#define ARDUBUS_DIGITAL_OUTPUTS { 13 }
#define ARDUBUS_ANALOG_INPUTS { A1 }
#define ARDUBUS_PWM_OUTPUTS { 13 }
#include <Servo.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_SERVO_OUTPUTS { 10 }
#include <I2C.h> // For some weird reason including this in the relevant .h file does not work
#define I2C_DEVICE_DEBUG
#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGB.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGBJBOL.h> // For some weird reason including this in the relevant .h file does not work
#define ARDUBUS_PCA9635RGBJBOL_BOARDS { 8 }

#include <ardubus.h>
void setup()
{
    Serial.begin(115200);
    ardubus_setup();
    Serial.println("Booted");
}

void loop()
{
    ardubus_update();
}
