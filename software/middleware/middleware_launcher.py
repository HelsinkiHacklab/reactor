#!/usr/bin/env python

import os,sys
import dbus
import dbus.service
import middleware

if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    instance = middleware.listener(bus, loop)

    loop.run()
