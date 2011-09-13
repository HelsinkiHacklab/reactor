# consumeservice.py
# consumes a method in a service on the dbus
 
import dbus
 
bus = dbus.SessionBus()
helloservice = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
hello = helloservice.get_dbus_method('hello', 'fi.hacklab.ardubus.hello')
print hello()