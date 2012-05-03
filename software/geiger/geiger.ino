/**
 * IRF9610 gate (pin 1) connected to OPIN, drain (pin 2) to speaker +, source (pin 3) to +5V (2A supply) and speaker - goes to ground.
 * Generic potentiometer to analog 1
 * analog 0 is floating to be used as random source.
 */

#define ANA0 3
#define ANA1 4
#define OPIN 1
#define PWMPIN 0
#define MIN_ACTIVITITY 15
// The P-channel needs to be driven this way or there will be a lot of heat
#define DRIVE_HI LOW
#define DRIVE_LO HIGH

int activity;

void setup()
{
    randomSeed(analogRead(0));
    pinMode(OPIN, OUTPUT);
    digitalWrite(OPIN, DRIVE_LO);
}

void pulse()
{
    digitalWrite(OPIN, DRIVE_HI);
    //delay(1);
    delayMicroseconds(400);
    digitalWrite(OPIN, DRIVE_LO);
}

int activity_adj(int activity)
{
    return (activity - 512) * 2;
}

byte pwm_adj(int activity)
{
    byte pwm = activity / 4;
    byte randb = random(0,10);
    if (pwm + randb < 255)
    {
        pwm += randb;
    }
    return pwm;
}

unsigned int loop_i;
void loop()
{
    loop_i++;
    // Reseed every ~16k loops
    if (loop_i == 0)
    {
        randomSeed(analogRead(ANA0));
    }
    activity = activity_adj(analogRead(ANA1));
    if (activity < MIN_ACTIVITITY)
    {
        activity = MIN_ACTIVITITY;
    }
    byte pwm = pwm_adj(activity); // PWM outputs are adjusted on 0-255 scale and mde to wobble a bit
    analogWrite(PWMPIN, pwm); 
    if (random(0, 2048) < activity) // even at 100% only pulse on 50% of cyles to get more random sound
    {
        pulse();
    }
    // This adjusts the general pulse rate (ie how fast 100% activity is, everything else is related to that)
    delay(30);
}
