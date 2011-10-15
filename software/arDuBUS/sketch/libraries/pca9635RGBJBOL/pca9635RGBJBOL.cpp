#include "pca9635RGB.h"

pca9635RGBJBOL::pca9635RGBJBOL()
{
}
pca9635RGBJBOL::~pca9635RGBJBOL()
{
}


// Proxies to all the individual drivers
boolean pca9635RGBJBOL::set_led_pwm(byte ledno, byte cycle)
{
    Serial.print("ledno/3=");
    Serial.println((byte)(ledno/3), DEC);
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
boolean pca9635RGBJBOL::set_led_mode(byte ledno, byte mode)
{
    boolean rstat = R.set_led_mode(ledno, mode);
    boolean gstat = G.set_led_mode(ledno, mode);
    boolean bstat = B.set_led_mode(ledno, mode);
    return rstat && gstat && bstat;
}
boolean pca9635RGBJBOL::set_led_mode(byte mode)
{
    boolean rstat = R.set_led_mode(mode);
    boolean gstat = G.set_led_mode(mode);
    boolean bstat = B.set_led_mode(mode);
    return rstat && gstat && bstat;
}
boolean pca9635RGBJBOL::set_driver_mode(byte mode)
{
    boolean rstat = R.set_driver_mode(mode);
    boolean gstat = G.set_driver_mode(mode);
    boolean bstat = B.set_driver_mode(mode);
    return rstat && gstat && bstat;
}
boolean pca9635RGBJBOL::set_sleep(byte sleep)
{
    boolean rstat = R.set_sleep(sleep);
    boolean gstat = G.set_sleep(sleep);
    boolean bstat = B.set_sleep(sleep);
    return rstat && gstat && bstat;
}
