// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


byte i2c_reg_values[8];

#include <Wire.h>

void setup()
{
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  // Enable the pull-ups
  digitalWrite(A4, HIGH);
  digitalWrite(A5, HIGH);
  Serial.begin(115200);           // start serial for output
}


unsigned long last_report;
void loop()
{
    unsigned long time = millis() - last_report;
    if (time > 5000)
    {
        last_report = millis();
        Serial.print(F("time="));
        Serial.println(time, DEC);
        for (byte i=0; i < sizeof(i2c_reg_values); i++)
        {
            Serial.print(F("i2c_reg_values["));
            Serial.print(i, DEC);
            Serial.print(F("]\t0x"));
            Serial.print(i2c_reg_values[i], HEX);
            Serial.print(F("\tB"));
            Serial.println(i2c_reg_values[i], BIN);
        }
    }
  
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
    Serial.print(F("receiveEvent("));
    Serial.print(howMany, DEC);
    Serial.println(F(")"));

    byte reg_addr = Wire.read();
    byte max_reg = reg_addr + howMany - 1;
    
    for (byte i = reg_addr; i < max_reg; i++)
    {
        i2c_reg_values[i] = Wire.read();
    }

    Serial.print(F("Complete"));
  /*
  while(1 < Wire.available()) // loop through all but the last
  {
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  int x = Wire.read();    // receive byte as an integer
  Serial.println(x);         // print the integer
  */
}
