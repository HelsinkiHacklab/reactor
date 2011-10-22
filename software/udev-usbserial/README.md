This directory has udev configuration to name serial ports by USB bus topology.

Install: make install

Uninstall: make uninstall

Example:

# find /dev/serial/by-topology
/dev/serial/by-topology
/dev/serial/by-topology/port3port1port3
/dev/serial/by-topology/port3port6
/dev/serial/by-topology/port3port3


In this example we have two external hubs and three serial ports (AVRs). Two AVRs are
connected to ports 3 and 6 of the first hub and one AVR is connected to the port 3 of
the second hub. The second hub is connected to the first port of the first hub.

