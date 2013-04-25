#ifndef ardubus_i2cascii_h
#define ardubus_i2cascii_h
#ifndef ARDUBUS_I2CASCII_BUFFER_SIZE
#define ARDUBUS_I2CASCII_BUFFER_SIZE 6 // 5 + null termination, size of the mwdisplay
#endif

/**
 * Trivial I2C addressed ASCII display, basically to support mwdisplay.ino but any "dumb" display
 * that will simply show what's in the registers will work.
 */

const byte ardubus_i2cascii_boards[] = ARDUBUS_I2CASCII_BOARDS;
char ardubus_i2cascii_buffer[ARDUBUS_I2CASCII_BUFFER_SIZE];

inline void ardubus_i2cascii_setup()
{
}

inline void ardubus_i2cascii_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_i2cascii_report()
{
    // PONDER: Do we need to report back the last value set and when it was set ??
}


inline void ardubus_i2cascii_process_command(char *incoming_command)
{
    switch(incoming_command[0])
    {
        case 0x77: // ASCII "w" (w<index><ascii>...<ascii>) //The index of ardubus_i2cascii_boards
            uint8_t addr = ardubus_i2cascii_boards[incoming_command[1]-ARDUBUS_INDEX_OFFSET];
            // This gives compiler error for some reason error:   initializing argument 2 of 'char* strncpy(char*, const char*, size_t)' [-fpermissive]
            strncpy(ardubus_i2cascii_buffer, incoming_command[2], ARDUBUS_I2CASCII_BUFFER_SIZE);
            
            // Write the buffer
            I2c.write(addr, 0x0, (uint8_t*)ardubus_i2cascii_buffer, (uint8_t)strlen(ardubus_i2cascii_buffer));

            Serial.print(F("w"));
            Serial.print(incoming_command[1]);
            Serial.print(ardubus_i2cascii_buffer);
            ardubus_ack();
            break;
    }
}

#endif