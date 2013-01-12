#define __PROG_TYPES_COMPAT__ 
#include <avr/pgmspace.h>
/**
 * Bit map for the display Hacklab Turku made
 * LOW bit means led on.
 *
 *        FD
 *       ----
 *     |      |
 *  7F |      | FB
 *     |  BF  |
 *       ----
 *     |      |
 *  DF |      | F7
 *     |      |
 *       ----
 *        EF
 *
 */
const prog_uchar asciitable_7seg_map[127] PROGMEM =
{
};


inline uint8_t ascii_to_7seg(uint8_t val)
{
    if (val > sizeof(asciitable_7seg_map))
    {
        // All off for invalid value
        return 0xff;
    }
    return pgm_read_byte_near(asciitable_7seg_map + val);
}

