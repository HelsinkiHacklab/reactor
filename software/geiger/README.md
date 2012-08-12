# Geiger counter simulator

Adjust radiation level from a potentiometer.

## BOM

  * ATTiny 85/45 on breakout board (see https://github.com/HelsinkiHacklab/aircores/blob/master/driver/attiny_bo_1l.brd)
    * Alternatively wire up the programming header and bypass cap to your board)
  * Small speaker
  * Potentiometer (preferably a slide one)
  * LM7805 or other 5V regulator (adjust wiring if pinout differs)
  * IRF740 N-channel MOSFET (or similar, a smaller one will probably be enough depending on your speaker)
  * 9V+ battery (more voltage -> more noise)
  * Generic parts (resistors, capacitators, wires, pin headers)
  * AVRISP mk 2 (for programming the attiny)

### Optional

  * Small analog voltage meter (preferably one with good or changeable background graphic), with separate backlight input (optional)
  * small leds to make a light for the display if it doesn't have one (optional), resistor for the leds to be used from 5V

## Assembly

  1. Make the ATTiny breakout board
  2. Wire up a board according to the wiring diagram
  3. The potentiometer is connected to the "MEASURE" header, third pin (white if using servo cables) should be connected to the wiper (middle), pins 1 (GND) and 2 (5V) to ends
  4. Speaker is connected to the "SPEAKER" header, note the polarity (pin 1 is GND)
  5. Experimentally figure out a good resistor for the voltmeter so that it's full on 5V and ~middle on 2.5V, connect it to the + terminal
  6. Wire up the volmeter light so that GND is common with the input GND
  7. Connect the voltmeter to the "METER" header, pin 1 is GND, pin 2 is backlight, pin 3 goes to voltmeter input.

## Programming

  1. Make sure you have installed the ATTiny cores to your Arduino IDE.
  2. power up the board without speaker attached (it will make very unpleasant noise when programming) and connect your AVRISP mk 2
  3. in Arduino select as board "ATTiny85 @8MHz (internal oscillator)"
  4. In tools select "Burn bootloader"
  5. Then upload the sketch

  



