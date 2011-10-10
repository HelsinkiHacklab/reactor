/**
 * IRF9610 gate (pin 1) connected to OPIN, drain (pin 2) to speaker +, source (pin 3) to +5V (2A supply) and speaker - goes to ground.
 * Generic potentiometer to analog 1
 * analog 0 is floating to be used as random source.
 */

#define OPIN 2
#define PWMPIN 10
// The P-channel needs to be driven this way or there will be a lot of heat
#define DRIVE_HI LOW
#define DRIVE_LO HIGH

byte activity = 15;

void setup()
{
    Serial.begin(115200);
    randomSeed(analogRead(0));
    pinMode(OPIN, OUTPUT);
    digitalWrite(OPIN, DRIVE_LO);
}

void pulse()
{
    Serial.println("pulse");
    digitalWrite(OPIN, DRIVE_HI);
    //delay(1);
    delayMicroseconds(500);
    digitalWrite(OPIN, DRIVE_LO);
}

unsigned int loop_i;
void loop()
{
    loop_i++;
    // Reseed every ~16k loops
    if (loop_i == 0)
    {
        randomSeed(analogRead(0));
    }
    activity = analogRead(1);
    analogWrite(PWMPIN, activity/4); // PWM outputs are adjusted on 0-255 scale.
    Serial.print("activity: ");
    Serial.println(activity, DEC);
    if (random(0, 1024) < activity)
    {
        pulse();
    }
    // This adjusts the max pulse rate
    delay(5);
}
