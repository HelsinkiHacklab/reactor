#!/usr/bin/env python

import gobject
import dbus
import dbus.service
import dbus.mainloop.glib


class ardubus(dbus.service.Object):
    def __init__(self, bus, object_name):
        object_path = '/fi/hacklab/ardubus/' + object_name
        dbus.service.Object.__init__(self, conn, object_path)




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
        service_objects[board_name] = ardubus(bus, board_name)

    loop = gobject.MainLoop()
    loop.run()