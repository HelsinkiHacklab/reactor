#ifndef ardubus_analog_in_h
#define ardubus_analog_in_h
#include <Arduino.h> 
#ifndef ARDUBUS_ANALOG_IN_UPDATE_TIME
#define ARDUBUS_ANALOG_IN_UPDATE_TIME 5 // Milliseconds, how often to check if inputs have changed
#endif


const uint8_t ardubus_analog_in_pins[] = ARDUBUS_ANALOG_INPUTS; // Analog inputs, unfiltered
int ardubus_analog_in_lastvals[sizeof(ardubus_analog_in_pins)]; // Store last value so we have at least the most rudimentary form of filtering for changes
unsigned long ardubus_analog_in_timestamps[sizeof(ardubus_analog_in_pins)]; // Store last change timestamp



inline void ardubus_analog_in_setup()
{
    for (uint8_t i=0; i < sizeof(ardubus_analog_in_pins); i++)
    {
        pinMode(ardubus_analog_in_pins[i], INPUT);
        digitalWrite(ardubus_analog_in_pins[i], LOW); // Make sure the internal pull-up is disabled
        ardubus_analog_in_lastvals[i] = analogRead(ardubus_analog_in_pins[i]);
    }
}

unsigned long ardubus_digital_in_last_read_time;
inline void ardubus_analog_in_read_inputs()
{
    for (uint8_t i=0; i < sizeof(ardubus_analog_in_pins); i++)
    {
        int tmp = analogRead(ardubus_analog_in_pins[i]);
        if (tmp != ardubus_analog_in_lastvals[i])
        {
            ardubus_analog_in_lastvals[i] = tmp;
            ardubus_analog_in_timestamps[i] = millis();
            Serial.print("CA"); // CA<index_uint8_t><value in hex>
            Serial.print(i);
            ardubus_print_int_as_4hex(ardubus_analog_in_lastvals[i]);
            Serial.println("");
        }
    }
    ardubus_digital_in_last_read_time = millis();
}

inline void ardubus_analog_in_update()
{
    if ((millis() - ardubus_digital_in_last_read_time) > ARDUBUS_ANALOG_IN_UPDATE_TIME)
    {
        ardubus_analog_in_read_inputs();
    }
}

inline void ardubus_analog_in_report()
{
    for (uint8_t i=0; i < sizeof(ardubus_analog_in_pins); i++)
    {
        Serial.print("RA"); // RA<index_uint8_t><value in hex>
        Serial.print(i);
        ardubus_print_int_as_4hex(ardubus_analog_in_lastvals[i]);
        ardubus_print_ulong_as_8hex(millis()-ardubus_analog_in_timestamps[i]);
        Serial.println("");
    }
}

inline void ardubus_analog_in_process_command(char *incoming_command)
{
    // This is a no-op (but defined so that all submodules have same API)
}


#endif
// *********** END OF CODE **********
