#!/usr/bin/env python

import os,sys,yaml
import dbus
import dbus.service
import middleware

if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    # Read config
    with open(__file__.replace('_launcher.py', '.yml')) as f:
        config = yaml.load(f)

    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    instance = middleware.ardubus_bridge(bus, loop, config)

    loop.run()
