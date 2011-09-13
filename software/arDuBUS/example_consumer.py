# consumeservice.py
# consumes a method in a service on the dbus
 
import dbus
 
bus = dbus.SessionBus()
helloservice = bus.get_object('org.frankhale.helloservice', '/org/frankhale/helloservice')
hello = helloservice.get_dbus_method('hello', 'org.frankhale.helloservice')
print hello()