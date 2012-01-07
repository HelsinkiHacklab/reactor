# -*- coding: utf-8 -*-

"""Ardubus object that works with QML object adhering to certain naming, see https://github.com/HelsinkiHacklab/reactor/tree/master/software/virtual_hardware/rodcontrol"""

import ardubus as ardubus_real
import dbus
import dbus.service
import dbus.mainloop.glib

class ardubus_qml(ardubus_real.ardubus):
    def __init__(self, bus, object_name, qml_proxy):
        self.qml_proxy = qml_proxy
        # Fake config for now
        import ConfigParser
        config = ConfigParser.SafeConfigParser()
        ardubus_real.ardubus.__init__(self, bus, object_name, config)

    def initialize_serial(self):
        print "Dummy serial"
        pass


    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_servo(self, servo_index, value):
        if value > 180:
            value = 180 # Servo library accepts values from 0 to 180 (degrees)
        if value in [ 13, 10]: #Offset values that map to CR or LF by one
            value += 1
        
        qml_object_name = self.object_name + "_servo" + str(int(servo_index))
        qml_object = self.qml_proxy.get_object(qml_object_name)
        if not qml_object:
            print "QML object %s not found" % qml_object_name
            return False
        qml_object.setPosition(int(value))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yn') # "y" is the signature for a byte, n is 16bit signed integer
    def set_servo_us(self, servo_index, value):
        qml_object_name = self.object_name + "_servo" + str(int(servo_index))
        qml_object = self.qml_proxy.get_object(qml_object_name)
        if not qml_object:
            print "QML object %s not found" % qml_object_name
            return False
        qml_object.setUSec(int(value))

if __name__ == '__main__':
    print "Use ardbus_launcher.py"
    sys.exit(1)
