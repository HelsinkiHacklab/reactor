#!/usr/bin/env python
import os,sys
import state
import dbus
import dbus.service

if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    # TODO: Add some nicer way to exit than ctrl-c
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    state_instance = state.state(bus, loop)
    state_instance.run()

