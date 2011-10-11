#ifndef ardubus_digital_out_h
#define ardubus_digital_out_h
#include <WProgram.h> 


inline void ardubus_digital_out_setup()
{
    // TODO: Implement
}

inline void ardubus_digital_out_update()
{
    // This is a no-op (but defined so that all submodules have same API)
}

inline void ardubus_digital_out_report()
{
    // TODO: Implement
}

inline void ardubus_digital_out_process_command(char *incoming_command)
{
    // TODO: Implement
    switch(incoming_command[0])
    {
    }
}


#endif
// *********** END OF CODE **********
