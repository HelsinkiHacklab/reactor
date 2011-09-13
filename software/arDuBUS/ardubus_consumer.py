# Trivial remote method call example (on two boards mainly to test the ardubus.py multi-board support)

import dbus
 
bus = dbus.SessionBus()
helloservice = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
hello = helloservice.get_dbus_method('hello', 'fi.hacklab.ardubus')
print hello()

helloservice = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino1')
hello = helloservice.get_dbus_method('hello', 'fi.hacklab.ardubus')
print hello()
