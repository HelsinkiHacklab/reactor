/**
 * IRF740 gate (pin 1) connected to OPIN, drain (pin 2) to speaker -, source (pin 3) to GND  and speaker + goes to supply voltage.
 * Generic potentiometer to analog 1
 * analog 0 is floating to be used as random source.
 */

/**
 * Pin notes by Suovula (see also http://hlt.media.mit.edu/?p=1229)
 *
// I2C
arduino pin 0 = not(OC1A) = PORTB <- _BV(0) = SOIC pin 5 (I2C SDA, PWM)
arduino pin 2 =           = PORTB <- _BV(2) = SOIC pin 7 (I2C SCL, Analog 1)
// Timer1 -> PWM
arduino pin 1 =     OC1A  = PORTB <- _BV(1) = SOIC pin 6 (PWM)
arduino pin 3 = not(OC1B) = PORTB <- _BV(3) = SOIC pin 2 (Analog 3)
arduino pin 4 =     OC1B  = PORTB <- _BV(4) = SOIC pin 3 (Analog 2)
 */

#define ANA0 A1
#define ANA1 A2
#define OPIN 1
#define PWMPIN 0
#define MIN_ACTIVITITY 15
// The P-channel needs to be driven this way or there will be a lot of heat (switched to NPN BJT)
#define DRIVE_HI HIGH
#define DRIVE_LO LOW

int activity;

inline void pulse()
{
    digitalWrite(OPIN, DRIVE_HI);
    //delay(1);
    delayMicroseconds(300);
    digitalWrite(OPIN, DRIVE_LO);
}

void setup()
{
    // TODO: Tri-state this and wait for input voltage to stabilize 
    pinMode(3, OUTPUT); // OC1B-, Arduino pin 3, ADC
    digitalWrite(3, LOW);


    pinMode(ANA0, INPUT);
    pinMode(ANA1, INPUT);
    randomSeed(analogRead(ANA0));
    pinMode(PWMPIN, OUTPUT);
    pinMode(OPIN, OUTPUT);

    pulse();


    digitalWrite(3, HIGH);
}


inline int activity_adj(int activity)
{
    //return activity;
    return (activity - 512) * 2;
}

inline byte pwm_adj(int activity)
{
    byte pwm = activity / 4;
    //return pwm;
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
    delay(15);
}
