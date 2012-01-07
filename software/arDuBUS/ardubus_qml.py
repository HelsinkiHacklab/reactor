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

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_pwm(self, pwm_index, cycle):
        qml_object_name = self.object_name + "_led" + str(int(pwm_index))
        qml_object = self.qml_proxy.get_object(qml_object_name)
        if not qml_object:
            print "QML object %s not found" % qml_object_name
            return False
        qml_object.setPWM(int(cycle))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yyy') # "y" is the signature for a byte
    def set_jbol_pwm(self, jbol_index, ledno, cycle):
        if cycle in [ 13, 10]: #Offset values that map to CR or LF by one
            cycle += 1
        qml_object_name = self.object_name + "_pca9635RGBJBOL" + str(int(jbol_index)) + "_led" + str(int(ledno))
        qml_object = self.qml_proxy.get_object(qml_object_name)
        if not qml_object:
            print "QML object %s not found" % qml_object_name
            return False
        qml_object.setPWM(int(cycle))

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

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yb') # "y" is the signature for a byte
    def set_595bit(self, bit_index, state):
        if state:
            pass
        else:
            pass

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_595byte(self, reg_index, state):
        pass

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yb') # "y" is the signature for a byte
    def set_dio(self, digital_index, state):
        # Only used for leds for now
        if state:
            self.set_pwm(digital_index, 255)
        else:
            self.set_pwm(digital_index, 0)

if __name__ == '__main__':
    print "Use ardbus_launcher.py"
    sys.exit(1)
