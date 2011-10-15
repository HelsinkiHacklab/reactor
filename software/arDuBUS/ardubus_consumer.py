#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
arduino0 = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
hello0 = arduino0.get_dbus_method('hello', 'fi.hacklab.ardubus')
pwm0 = arduino0.get_dbus_method('set_pwm', 'fi.hacklab.ardubus')
dio0 = arduino0.get_dbus_method('set_dio', 'fi.hacklab.ardubus')
servo0 = arduino0.get_dbus_method('set_servo', 'fi.hacklab.ardubus')
jbol0 = arduino0.get_dbus_method('set_jbol_pwm', 'fi.hacklab.ardubus')
print hello0()
pwm0(0,128)


