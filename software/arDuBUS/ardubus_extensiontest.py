#!/usr/bin/env python

# A class for testing extending the baseclass

import os, random
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
import ardubus as ardubus_real

class ardubus(ardubus_real.ardubus):
    def __init__(self, bus, object_name, config):
        ardubus_real.ardubus.__init__(self, bus, object_name, config)
        gobject.timeout_add(5000, self.random_pwm)

    def random_pwm(self):
        self.set_pwm(0, random.randint(5,250))
        # We must return true to keep this interval running
        return True


if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
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
