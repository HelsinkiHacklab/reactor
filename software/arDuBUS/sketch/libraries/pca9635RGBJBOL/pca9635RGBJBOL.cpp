#include "pca9635RGBJBOL.h"

// Proxies to all the individual drivers
uint8_t pca9635RGBJBOL::set_led_pwm(uint8_t ledno, byte cycle)
{
    switch (ledno%3)
    {
        case 0:
            return R.set_led_pwm(ledno/3, cycle);
            break;
        case 1:
            return G.set_led_pwm(ledno/3, cycle);
            break;
        case 2:
            return B.set_led_pwm(ledno/3, cycle);
            break;
    }
}
uint8_t pca9635RGBJBOL::set_led_mode(uint8_t ledno, byte mode)
{
    uint8_t rstat = R.set_led_mode(ledno, mode);
    uint8_t gstat = G.set_led_mode(ledno, mode);
    uint8_t bstat = B.set_led_mode(ledno, mode);
    return rstat && gstat && bstat;
}
uint8_t pca9635RGBJBOL::set_led_mode(uint8_t mode)
{
    uint8_t rstat = R.set_led_mode(mode);
    uint8_t gstat = G.set_led_mode(mode);
    uint8_t bstat = B.set_led_mode(mode);
    return rstat && gstat && bstat;
}
uint8_t pca9635RGBJBOL::set_driver_mode(uint8_t mode)
{
    uint8_t rstat = R.set_driver_mode(mode);
    uint8_t gstat = G.set_driver_mode(mode);
    uint8_t bstat = B.set_driver_mode(mode);
    return rstat && gstat && bstat;
}
uint8_t pca9635RGBJBOL::set_sleep(uint8_t sleep)
{
    uint8_t rstat = R.set_sleep(sleep);
    uint8_t gstat = G.set_sleep(sleep);
    uint8_t bstat = B.set_sleep(sleep);
    return rstat && gstat && bstat;
}
