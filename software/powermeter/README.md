# Console power meter

ATTiny84 displaying on LCD the voltages and currents on the 5V and 3.3V power buses of the rod control console.

Standard hitachi-style 2x16 LCD module, two Pololu current sensors (due to availability two different ones: [ACS714][1] & [ACS715][2])

This is wired up on stripboard, I'll draw a schematic when I get around to it (TODO: add 1M pull-downs to all the sensor lines).

The ACS714 (red X) goes to right-side connectors, ACS715 (black X) to left, remember that the measurement return pin is on that side of the connector too.

[1]: http://www.pololu.com/catalog/product/1187
[2]: http://www.pololu.com/catalog/product/1186

