#!/usr/bin/env python

import os, random
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
import ardubus as ardubus_real

class ardubus(ardubus_real.ardubus):
    def __init__(self, bus, object_name, config):
        ardubus_real.ardubus.__init__(self, bus, object_name, config)
        gobject.timeout_add(1000, self.random_event)

    def initialize_serial(self):
        print "Dummy serial"
        pass

    def random_event(self):
        # TODO: Fire a random signal
        self.dio_change(random.randint(2,8), random.randint(0,1), self.object_name)

        # We must return true to keep this interval running
        return True

    


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    import ConfigParser
    config = ConfigParser.SafeConfigParser()
    if not os.path.isfile('ardubus.conf'):
        config.add_section('arduino0')
        config.set('arduino0', 'device', '/dev/ttyUSB0')
        # TODO: Other defaults
        with open('ardubus.conf', 'wb') as configfile:
            config.write(configfile)
    config.read('ardubus.conf')

    bus = dbus.SessionBus()

    service_objects = {}
    for board_name in config.sections():
        service_objects[board_name] = ardubus(bus, board_name, config)

    loop = gobject.MainLoop()
    loop.run()
